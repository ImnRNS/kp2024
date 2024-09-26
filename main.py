from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('user/home.html')

@app.route("/gallery")
def gallery():
    return render_template('user/gallery.html')
 
@app.route("/order")
def order():
    return render_template('user/order.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
