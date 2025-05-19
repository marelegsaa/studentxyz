from flask import Flask, render_template, url_for, request, redirect, session, flash, jsonify
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Nota

import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 587))
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

with app.app_context():
    db.init_app(app)
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            if not user.confirmed:
                flash('contul nu este confirmat. verifică-ți emailul pentru a-l confirma.', 'error')
                return redirect(url_for('login'))
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
    if request.method == 'GET':
        return render_template('login/signup.html')
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

        token = serializer.dumps(email, salt="email-confirm")
        confirm_url = url_for('confirm_email', token=token, _external=True)

        msg = Message('confirmă-ți contul studentxyz',
              sender=app.config['MAIL_USERNAME'],
              recipients=[email])
        msg.body = f'mulțumim că te-ai înregistrat!\nda click pe linkul următor pentru a confirma contul:\n{confirm_url}'
        msg.html = f'''
<html>
<body>
  <div style="font-family: Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; color: #333; line-height: 1.6;">
    <div style="background-color: #e0e0e0; padding: 30px 20px 20px; border-radius: 0 0 10px 10px; text-align: center;">
      <img src="https://i.imgur.com/qPeqmKv.png" alt="logo" style="width: 320px; height: auto; display: block; margin: 0 auto;">
    </div>

    <div style="max-width: 600px; margin: 30px auto; background: white; padding: 30px 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); text-align: center;">
      <h2 style="font-size: 24px; margin-bottom: 15px;">mulțumim că te-ai înregistrat!</h2>
      <p style="font-size: 18px; margin-bottom: 25px;">pentru a-ți confirma contul, te rugăm să dai click pe butonul de mai jos:</p>
      <a href="{confirm_url}" style="display: inline-block; padding: 12px 24px; background-color: #181818; color: #fff; text-decoration: none; font-weight: bold; border-radius: 6px; font-size: 16px;">confirmă contul</a>
      <p style="font-size: 16px; margin-top: 25px;">dacă nu ai solicitat acest cont, poți ignora acest email.</p>
    </div>

    <div style="background-color: #e0e0e0; color: #555; font-size: 13px; padding: 15px 10px; text-align: center;">
      &copy; 2025 marelegsaa - all rights reserved.
    </div>
  </div>
</body>
</html>
        '''
        mail.send(msg)

        flash('cont creat! verifică-ți emailul pentru a confirma contul.', 'info')
        return redirect(url_for('login'))

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt="email-confirm", max_age=3600)
    except:
        flash('link invalid sau expirat.', 'error')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('utilizator inexistent.', 'error')
    elif user.confirmed:
        flash('contul este deja confirmat.', 'info')
    else:
        user.confirmed = True
        db.session.commit()
        flash('cont confirmat cu succes!', 'success')
    return redirect(url_for('login'))

    return render_template('login/signup.html')

import random
import string

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if "username" in session:
        return redirect(url_for('dashboard'))
    if request.method == 'GET':
        return render_template('login/reset.html')
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if not user:
            flash('email-ul nu este înregistrat!', 'error')
            return redirect(url_for('reset'))

        new_password = generate_random_password()
        user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        db.session.commit()

        msg = Message('parola ta nouă studentxyz',
              sender=app.config['MAIL_USERNAME'],
              recipients=[email])
        msg.body = f'parola ta nouă este: {new_password}\nte rugăm să o schimbi după ce te autentifici.'
        msg.html = f'''
<html>
<body>
  <div style="font-family: Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; color: #333; line-height: 1.6;">
    <div style="background-color: #e0e0e0; padding: 30px 20px 20px; border-radius: 0 0 10px 10px; text-align: center;">
      <img src="https://i.imgur.com/qPeqmKv.png" alt="logo" style="width: 320px; height: auto; display: block; margin: 0 auto;">
    </div>

    <div style="max-width: 600px; margin: 30px auto; background: white; padding: 30px 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); text-align: center;">
      <h2 style="font-size: 24px; margin-bottom: 15px;">noua ta parolă este: </h2>
      <span style="font-size: 27px; font-weight: bold; color: #2d7a2d; margin-bottom: 20px;">{new_password}</span>
      <p style="font-size: 16px; margin-top: 25px;">te rugăm să o schimbi după ce te autentifici.</p>
    </div>

    <div style="background-color: #e0e0e0; color: #555; font-size: 13px; padding: 15px 10px; text-align: center;">
      &copy; 2025 marelegsaa - all rights reserved.
    </div>
  </div>
</body>
</html>
        '''
        mail.send(msg)

        flash('email trimis! verifică-ți inbox-ul pentru parola nouă.', 'info')
        return redirect(url_for('login'))
    
@app.route('/save_nota', methods=['POST'])
def save_nota():
    if "user_id" not in session:
        return redirect(url_for('login'))

    data = request.get_json()
    an = data['an']
    semestru = data['semestru']
    materie = data['materie']
    nota = data['nota']
    user_id = session['user_id']

    nota_existenta = Nota.query.filter_by(
        user_id=user_id,
        an=an,
        semestru=semestru,
        materie=materie
    ).first()

    if nota_existenta:
        nota_existenta.nota = nota
    else:
        new_nota = Nota(user_id=user_id, an=an, semestru=semestru, materie=materie, nota=nota)
        db.session.add(new_nota)

    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if "username" not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    specializare = session['specializare']

    note = Nota.query.filter_by(user_id=user_id).all()

    note_dict = {}
    for nota in note:
        key = f"{nota.an}-{nota.semestru}-{nota.materie}"
        note_dict[key] = nota.nota

    return render_template('homepage/dashboard.html', specializare=specializare, note=note_dict)

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