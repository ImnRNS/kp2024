import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")  # Secret key for session management

# Get MongoDB URI and database name from environment variables
MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

# Initialize MongoDB client
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]  # Access the specific database

@app.route('/')
def home():
    """Render the home page."""
    return render_template('user/home.html')

@app.route("/gallery")
def gallery():
    """Render the gallery page."""
    return render_template('user/gallery.html')

@app.route("/order")
def order():
    """Render the order page."""
    return render_template('user/order.html')

@app.route("/masuk", methods=['GET'])
def masuk():
    """Render the login page."""
    return render_template('user/masuk.html', msg=None)  # Pass initial msg as None

@app.route("/register", methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Perform validation checks
        if not name or not email or not password:
            msg = 'All fields are required!'
            return render_template('user/register.html', msg=msg)

        # Hash the password before storing
        hashed_password = generate_password_hash(password)

        # Save user data to the database
        user_data = {
            'name': name,
            'email': email,
            'password': hashed_password  # Store hashed password
        }
        
        # Check if the user already exists
        if db.users.find_one({'email': email}):
            msg = 'Email already registered!'
            return render_template('user/register.html', msg=msg)

        db.users.insert_one(user_data)  # Insert the user data into the 'users' collection
        msg = 'Registration successful!'
        return render_template('user/masuk.html', msg=msg)  # Redirect to login page after successful registration

    return render_template('user/register.html', msg=None)  # Render registration page

@app.route("/login", methods=['POST'])
def login():
    """Handle user login."""
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Find user by email
    user = db.users.find_one({'email': email})
    
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['_id']  # Store user ID in session
        msg = 'Login successful!'
        return render_template('user/home.html', msg=msg)  # Redirect to home after successful login
    else:
        msg = 'Invalid email or password!'
        return render_template('user/masuk.html', msg=msg)  # Redirect back to login page on failure

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
