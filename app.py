from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def login():
    return render_template("login/login.html")
@app.route('/home')
def home():
    return render_template("homepage/home.html")
@app.route('/signup')
def signup():
    return render_template('login/signup.html')
@app.route('/reset')
def reset():
    return render_template('login/reset.html')
if __name__ == "__main__":
    app.run(debug=True)

