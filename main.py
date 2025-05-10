from flask import Flask, render_template, url_for, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(100), nullable=False)
    prenume = db.Column(db.String(100), nullable=False)
    facultate = db.Column(db.String(100), nullable=False)
    specializare = db.Column(db.String(100), nullable=False)
    an = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['username'] = user.email
            session['user_id'] = user.id
            session['specializare'] = user.specializare 
            return redirect(url_for('dashboard'))
        else:
            flash('email sau parolă incorectă', 'error')
    
    return render_template('login/login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if "username" in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        nume = request.form.get('nume')
        prenume = request.form.get('prenume')
        facultate = request.form.get('facultate')
        specializare = request.form.get('specializare')
        an = request.form.get('an')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not email.endswith('@stud.ase.ro'):
            flash('trebuie să folosești un email instituțional (@stud.ase.ro)', 'error')
            return redirect(url_for('signup'))
        
        if password != confirm_password:
            flash('parolele nu coincid!', 'error')
            return redirect(url_for('signup'))
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('acest email este deja înregistrat!', 'error')
            return redirect(url_for('signup')) 
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = User(
            nume=nume,
            prenume=prenume,
            facultate=facultate,
            specializare=specializare,
            an=an,
            email=email,
            password=hashed_password
        )
        
        db.session.add(new_user)
        db.session.commit()

        flash('cont creat cu succes!', 'success')
        return redirect(url_for('login'))
    
    return render_template('login/signup.html')

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if "username" in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:

            flash('un email de resetare a parolei a fost trimis (simulat)', 'info')
        else:
            flash('acest email nu este înregistrat!', 'error')
        return redirect(url_for('login'))
    
    return render_template('login/reset.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if "username" not in session:
        return redirect(url_for('login'))
    print(session['specializare'])
    return render_template('homepage/dashboard.html', specializare=session['specializare'])

@app.route('/analytics')
def analytics():
    if "username" not in session:
        return redirect(url_for('login'))
    return render_template('homepage/analytics.html')

@app.route('/settings')
def settings():
    if "username" not in session:
        return redirect(url_for('login'))
    return render_template('homepage/settings.html')

@app.route('/user')
def user():
    if "username" not in session:
        return redirect(url_for('login'))
    return render_template('homepage/user.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)