from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def login():
    return render_template("login/login.html")
@app.route('/signup')
def signup():
    return render_template('login/signup.html')
@app.route('/reset')
def reset():
    return render_template('login/reset.html')
@app.route('/dashboard')
def dashboard():
    return render_template("homepage/dashboard.html")
@app.route('/analytics')
def analytics():
    return render_template('homepage/analytics.html')
@app.route('/settings')
def settings():
    return render_template('homepage/settings.html')
@app.route('/user')
def user():
    return render_template('homepage/user.html')

if __name__ == "__main__":
    app.run(debug=True)

