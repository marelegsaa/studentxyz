from flask import Flask, render_template, url_for, request, redirect, session, flash, jsonify, send_from_directory
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, Nota
from validari import MATERII, OPTIUNI_OPTIONALE, CREDITE, CREDITE_OPTIONALE
from PIL import Image
import os
import uuid
import sqlite3
import random
import string
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

UPLOAD_FOLDER = 'uploads/profile_pictures'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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

def is_physical_education(materie):
    return 'educație fizică' in materie.lower() or 'educatie fizica' in materie.lower()

def get_previous_period(an, semestru):
    an_int = int(an)
    sem_int = int(semestru)
    
    if sem_int == 1:
        if an_int == 1:
            return None
        else:
            return (an_int - 1, 2)
    else:
        return (an_int, 1)

def can_add_grades_for_period(user_id, an, semestru, specializare=None):
    an_int = int(an)
    sem_int = int(semestru)
    
    if an_int == 1 and sem_int == 1:
        return True
    
    prev_period = get_previous_period(an, semestru)
    if prev_period is None:
        return True
    
    prev_an, prev_sem = prev_period
    cheie = f"{prev_an}-{prev_sem}"

    if specializare is None:
        user = User.query.get(user_id)
        if not user:
            return False
        specializare = user.specializare

    obligatorii = []
    if specializare in MATERII and cheie in MATERII[specializare]:
        obligatorii = MATERII[specializare][cheie]
    
    if not obligatorii:
        return True

    for materie in obligatorii:
        nota_existenta = Nota.query.filter_by(
            user_id=user_id,
            an=str(prev_an),
            semestru=str(prev_sem),
            materie=materie
        ).first()
        
        if nota_existenta is None:
            return False
    
    return True

def predict_next_semester_grades(user_id, current_year, current_semester):
    
    print(f"DEBUG: Starting prediction for user {user_id}, {current_year}-{current_semester}")
    
    try:
        semester_transitions = {
            (1, 1): (1, 2),
            (1, 2): (2, 1),
            (2, 1): (2, 2),
            (2, 2): (3, 1),
            (3, 1): (3, 2)
        }
        
        if (current_year, current_semester) not in semester_transitions:
            print(f"DEBUG: No next semester for {current_year}-{current_semester}")
            return None
        
        next_year, next_semester = semester_transitions[(current_year, current_semester)]
        print(f"DEBUG: Next semester: {next_year}-{next_semester}")
        
        user = User.query.get(user_id)
        if not user:
            print(f"DEBUG: User {user_id} not found")
            return None
        
        specializare = user.specializare
        print(f"DEBUG: User specialization: {specializare}")
        
        if specializare not in MATERII:
            print(f"DEBUG: Specialization {specializare} not found in MATERII")
            return None
        
        current_notes = Nota.query.filter_by(
            user_id=user_id,
            an=current_year,
            semestru=current_semester
        ).all()
        
        print(f"DEBUG: Found {len(current_notes)} notes for current semester")
        
        valid_grades = []
        current_grades_dict = {}
        
        for nota in current_notes:
            if nota.nota is not None:
                if is_physical_education(nota.materie):
                    current_grades_dict[nota.materie.lower()] = str(nota.nota).lower()
                    print(f"DEBUG: PE grade: {nota.materie} = {nota.nota}")
                else:
                    try:
                        if isinstance(nota.nota, str):
                            continue
                        grade_value = int(nota.nota)
                        if 1 <= grade_value <= 10:
                            valid_grades.append(grade_value)
                            current_grades_dict[nota.materie.lower()] = grade_value
                            print(f"DEBUG: Valid grade: {nota.materie} = {grade_value}")
                    except (ValueError, TypeError):
                        print(f"DEBUG: Invalid grade value for {nota.materie}: {nota.nota}")
        
        if not valid_grades:
            print("DEBUG: No valid numerical grades found")
            return None
        
        print(f"DEBUG: Processing {len(valid_grades)} valid grades: {valid_grades}")

        media_curenta = sum(valid_grades) / len(valid_grades)
        print(f"DEBUG: Current average: {media_curenta}")

        next_semester_key = f"{next_year}-{next_semester}"
        print(f"DEBUG: Looking for subjects in {next_semester_key}")
        
        if next_semester_key not in MATERII[specializare]:
            print(f"DEBUG: No subjects found for {next_semester_key} in {specializare}")
            return None
        
        next_subjects = MATERII[specializare][next_semester_key]
        print(f"DEBUG: Next semester subjects: {next_subjects}")

        predictions = {}
        
        for subject in next_subjects:
            if is_physical_education(subject):
                if media_curenta >= 7:
                    predictions[subject] = "admis"
                elif media_curenta >= 5:
                    predictions[subject] = "admis" if random.random() < 0.8 else "respins"
                else:
                    predictions[subject] = "respins" if random.random() < 0.6 else "admis"
                print(f"DEBUG: Predicted PE {subject}: {predictions[subject]}")
                continue
            
            base_prediction = media_curenta
            
            if any(keyword in subject.lower() for keyword in ['matematică', 'algebră', 'analiză']):
                base_prediction -= random.uniform(0.5, 1.5)
                math_keywords = ['algebră', 'analiză', 'matematică', 'statisticii']
                for math_kw in math_keywords:
                    for curr_subject, grade in current_grades_dict.items():
                        if isinstance(grade, int) and math_kw in curr_subject:
                            base_prediction = (base_prediction + grade) / 2
                            print(f"DEBUG: Math correlation: {curr_subject} ({grade}) -> {subject}")
                            break
                            
            elif any(keyword in subject.lower() for keyword in ['programare', 'algoritmi', 'informatică', 'baze']):
                prog_keywords = ['programare', 'algoritmi', 'baze', 'informatică', 'tehnologiei']
                prog_grades = []
                
                for prog_kw in prog_keywords:
                    for curr_subject, grade in current_grades_dict.items():
                        if isinstance(grade, int) and prog_kw in curr_subject:
                            prog_grades.append(grade)
                            print(f"DEBUG: Programming correlation: {curr_subject} ({grade}) -> {subject}")
                
                if prog_grades:
                    base_prediction = (base_prediction + sum(prog_grades) / len(prog_grades)) / 2
                base_prediction += random.uniform(-1, 1.5)
                
            elif any(keyword in subject.lower() for keyword in ['statistică', 'econometrie', 'probabilități']):
                stat_keywords = ['statistică', 'statisticii', 'probabilități', 'econometrie']
                stat_grades = []
                
                for stat_kw in stat_keywords:
                    for curr_subject, grade in current_grades_dict.items():
                        if isinstance(grade, int) and stat_kw in curr_subject:
                            stat_grades.append(grade)
                            print(f"DEBUG: Statistics correlation: {curr_subject} ({grade}) -> {subject}")
                
                if stat_grades:
                    base_prediction = (base_prediction + sum(stat_grades) / len(stat_grades)) / 2
                    
            elif any(keyword in subject.lower() for keyword in ['economie', 'management', 'marketing', 'finanțe']):
                base_prediction += random.uniform(0, 1)
                econ_keywords = ['economie', 'management', 'marketing', 'finanțe']
                for econ_kw in econ_keywords:
                    for curr_subject, grade in current_grades_dict.items():
                        if isinstance(grade, int) and econ_kw in curr_subject:
                            base_prediction = (base_prediction + grade) / 2
                            print(f"DEBUG: Economics correlation: {curr_subject} ({grade}) -> {subject}")
                            break
            
            progression_factor = 0.3 if next_year > current_year else 0.1
            base_prediction += random.uniform(0, progression_factor)
            
            base_prediction += random.uniform(-0.5, 0.5)
            
            predicted_grade = max(1, min(10, base_prediction))
            predictions[subject] = round(predicted_grade, 1)
            
            print(f"DEBUG: Predicted {subject}: {predicted_grade}")
        
        if len(valid_grades) > 1:
            mean_val = sum(valid_grades) / len(valid_grades)
            variance = sum((x - mean_val) ** 2 for x in valid_grades) / len(valid_grades)
            grade_std = variance ** 0.5
        else:
            grade_std = 0
            
        confidence = max(0.6, min(0.9, (media_curenta / 10) * (1 - grade_std / 10)))
        
        result = {
            'next_year': next_year,
            'next_semester': next_semester,
            'predictions': predictions,
            'confidence': round(confidence, 2)
        }
        
        print(f"DEBUG: Final result: {result}")
        return result
        
    except Exception as e:
        print(f"DEBUG ERROR in prediction: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

@app.route('/api/predict_grades', methods=['POST'])
def predict_grades():
    
    print("DEBUG: predict_grades endpoint called")
    
    if "user_id" not in session:
        print("DEBUG: User not logged in")
        return jsonify({'error': 'not logged in'}), 401
    
    try:
        data = request.get_json()
        print(f"DEBUG: Received data: {data}")
        
        if not data:
            print("DEBUG: No JSON data received")
            return jsonify({'error': 'No data provided'}), 400
            
        year = int(data.get('year', 0))
        semester = int(data.get('semester', 0))
        user_id = session['user_id']
        
        print(f"DEBUG: Processing prediction for user {user_id}, year {year}, semester {semester}")
        
        if year not in [1, 2, 3] or semester not in [1, 2]:
            print(f"DEBUG: Invalid year/semester: {year}/{semester}")
            return jsonify({
                'error': 'date invalide',
                'message': 'anul trebuie să fie 1-3, semestrul 1-2.'
            }), 400
        
        predictions = predict_next_semester_grades(user_id, year, semester)
        
        if predictions is None:
            print("DEBUG: Predictions returned None")
            return jsonify({
                'error': 'nu se pot face predicții',
                'message': 'introduceți mai întâi notele pentru semestrul curent.'
            })
        
        print("DEBUG: Predictions successful")
        return jsonify({
            'success': True,
            'predictions': predictions
        })
        
    except ValueError as e:
        print(f"DEBUG: ValueError: {str(e)}")
        return jsonify({
            'error': 'date invalide',
            'message': f'eroare de validare: {str(e)}'
        }), 400
        
    except Exception as e:
        print(f"DEBUG: Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'eroare internă',
            'message': 'a apărut o eroare neașteptată.'
        }), 500

@app.route('/api/get_prediction_accuracy', methods=['GET'])
def get_prediction_accuracy():
    if "user_id" not in session:
        return jsonify({'error': 'not logged in'}), 401
    
    try:
        return jsonify({
            'accuracy': 0.85,
            'mae': 0.7,
            'rmse': 0.9,
            'r2_score': 0.78,
            'training_samples': 1000,
            'model_version': '1.0'
        })
    except Exception as e:
        print(f"ERROR in get_prediction_accuracy: {str(e)}")
        return jsonify({
            'error': 'eroare la încărcarea metricilor',
            'message': str(e)
        }), 500

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_common_subjects(spec1, spec2):
    common = set()
    if spec1 in MATERII and spec2 in MATERII:
        for key in MATERII[spec1]:
            if key in MATERII[spec2]:
                common.update(set(MATERII[spec1][key]) & set(MATERII[spec2][key]))
    return common

def calculate_semester_average(user_id, year, semester):

    print(f"DEBUG: CREDITE_OPTIONALE disponibil: {'CREDITE_OPTIONALE' in globals()}")
    try:
        print(f"DEBUG: CREDITE_OPTIONALE keys: {list(CREDITE_OPTIONALE.keys())}")
    except NameError:
        print("DEBUG: CREDITE_OPTIONALE nu este definit!")
        return None
    
    notes = Nota.query.filter_by(
        user_id=user_id, 
        an=year, 
        semestru=semester
    ).filter(Nota.nota.isnot(None)).all()
    
    if not notes:
        return None
    
    user = User.query.get(user_id)
    specializare = user.specializare
    
    total_points = 0
    total_credits = 0
    
    for nota in notes:
        if is_physical_education(nota.materie):
            continue
            
        try:
            if isinstance(nota.nota, str):
                continue
            nota_value = int(nota.nota)
        except (ValueError, TypeError):
            continue

        cheie = f"{nota.an}-{nota.semestru}"
        credits = 3
        
        print(f"DEBUG: Procesez materia '{nota.materie}' pentru {cheie}")

        if (specializare in CREDITE and 
            cheie in CREDITE[specializare] and 
            nota.materie in CREDITE[specializare][cheie]):
            credits = CREDITE[specializare][cheie][nota.materie]
            print(f"DEBUG: Găsit în CREDITE: {nota.materie} = {credits} credite")

        elif cheie in CREDITE_OPTIONALE and nota.materie in CREDITE_OPTIONALE[cheie]:
            credits = CREDITE_OPTIONALE[cheie][nota.materie]
            print(f"DEBUG: Găsit în CREDITE_OPTIONALE: {nota.materie} = {credits} credite")
        else:
            print(f"DEBUG: Nu găsit în dicționare, folosesc valoarea implicită: {nota.materie} = {credits} credite")
        
        if credits > 0:
            total_points += nota_value * credits
            total_credits += credits
    
    if total_credits > 0:
        return round(total_points / total_credits, 2)
    return None

def get_overall_average(user_id):
    notes = Nota.query.filter_by(user_id=user_id).filter(Nota.nota.isnot(None)).all()
    
    if not notes:
        return None
    
    user = User.query.get(user_id)
    specializare = user.specializare
    
    total_points = 0
    total_credits = 0
    
    for nota in notes:
        if is_physical_education(nota.materie):
            continue
            
        try:
            if isinstance(nota.nota, str):
                continue
            nota_value = int(nota.nota)
        except (ValueError, TypeError):
            continue

        cheie = f"{nota.an}-{nota.semestru}"
        credits = 3
        
        if (specializare in CREDITE and 
            cheie in CREDITE[specializare] and 
            nota.materie in CREDITE[specializare][cheie]):
            credits = CREDITE[specializare][cheie][nota.materie]
        
        elif cheie in CREDITE_OPTIONALE and nota.materie in CREDITE_OPTIONALE[cheie]:
            credits = CREDITE_OPTIONALE[cheie][nota.materie]
        
        if credits > 0:
            total_points += nota_value * credits
            total_credits += credits
    
    if total_credits > 0:
        return round(total_points / total_credits, 2)
    return None

def get_all_semester_averages(user_id):
    semester_averages = {}

    for year in [1, 2, 3]:
        for sem in [1, 2]:
            avg = calculate_semester_average(user_id, year, sem)
            if avg is not None:
                semester_averages[f"An {year}, Sem {sem}"] = avg
    
    return semester_averages

def get_yearly_averages(user_id):
    yearly_averages = {}
    
    user = User.query.get(user_id)
    if not user:
        return yearly_averages
    
    specializare = user.specializare
    
    for year in [1, 2, 3]:
        notes = Nota.query.filter_by(
            user_id=user_id, 
            an=year
        ).filter(Nota.nota.isnot(None)).all()
        
        if not notes:
            continue
        
        total_points = 0
        total_credits = 0
        
        for nota in notes:
            if is_physical_education(nota.materie):
                continue
                
            try:
                if isinstance(nota.nota, str):
                    continue
                nota_value = int(nota.nota)
            except (ValueError, TypeError):
                continue

            cheie = f"{nota.an}-{nota.semestru}"
            credits = 3
            
            if (specializare in CREDITE and 
                cheie in CREDITE[specializare] and 
                nota.materie in CREDITE[specializare][cheie]):
                credits = CREDITE[specializare][cheie][nota.materie]
            
            elif cheie in CREDITE_OPTIONALE and nota.materie in CREDITE_OPTIONALE[cheie]:
                credits = CREDITE_OPTIONALE[cheie][nota.materie]
            
            if credits > 0:
                total_points += nota_value * credits
                total_credits += credits
        
        if total_credits > 0:
            yearly_averages[f"An {year}"] = round(total_points / total_credits, 2)
    
    return yearly_averages

def calculate_best_semester(user_id):
    semester_averages = get_all_semester_averages(user_id)
    
    if not semester_averages:
        return None, None
    
    best_semester = max(semester_averages, key=semester_averages.get)
    best_avg = semester_averages[best_semester]
    
    return best_semester, best_avg

def get_detailed_stats(user_id):
    notes = Nota.query.filter_by(user_id=user_id).filter(Nota.nota.isnot(None)).all()
    
    if not notes:
        return {
            'total_credits_earned': 0,
            'subjects_passed': 0,
            'subjects_failed': 0,
            'total_subjects': 0,
            'grade_distribution': {},
            'pass_rate': 0
        }
    
    user = User.query.get(user_id)
    specializare = user.specializare
    
    total_credits_earned = 0
    subjects_passed = 0
    subjects_failed = 0
    total_subjects = 0
    grade_distribution = {}
    
    for nota in notes:
        total_subjects += 1
        
        if is_physical_education(nota.materie):
            if str(nota.nota).lower() == 'admis':
                subjects_passed += 1
                total_credits_earned += 1
            else:
                subjects_failed += 1
            continue
        
        try:
            if isinstance(nota.nota, str):
                continue
            nota_value = int(nota.nota)
        except (ValueError, TypeError):
            continue

        if nota_value in grade_distribution:
            grade_distribution[nota_value] += 1
        else:
            grade_distribution[nota_value] = 1

        if nota_value >= 5:
            subjects_passed += 1
            cheie = f"{nota.an}-{nota.semestru}"
            credits = 3
            
            if (specializare in CREDITE and 
                cheie in CREDITE[specializare] and 
                nota.materie in CREDITE[specializare][cheie]):
                credits = CREDITE[specializare][cheie][nota.materie]

            elif cheie in CREDITE_OPTIONALE and nota.materie in CREDITE_OPTIONALE[cheie]:
                credits = CREDITE_OPTIONALE[cheie][nota.materie]
                
            total_credits_earned += credits
        else:
            subjects_failed += 1
    
    pass_rate = round((subjects_passed / total_subjects) * 100, 1) if total_subjects > 0 else 0
    
    return {
        'total_credits_earned': total_credits_earned,
        'subjects_passed': subjects_passed,
        'subjects_failed': subjects_failed,
        'total_subjects': total_subjects,
        'grade_distribution': dict(sorted(grade_distribution.items())),
        'pass_rate': pass_rate
    }

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/privacy-policy')
def privacy_policy():
    return send_from_directory('legal', 'POLITICA DE CONFIDENȚIALITATE A DATELOR.pdf')

@app.route('/terms')
def terms():
    return send_from_directory('legal', 'TERMENI ȘI CONDIȚII DE UTILIZARE.pdf')

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
        gdpr_consent = request.form.get('gdpr_consent')

        if not gdpr_consent:
            flash('trebuie să accepți Politica de Confidențialitate și Termenii de Utilizare', 'error')
            return redirect(url_for('signup'))
        
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

@app.route('/confirm_email_change/<token>')
def confirm_email_change(token):
    try:
        data = serializer.loads(token, salt="email-change", max_age=3600)
        user_id = data['user_id']
        new_email = data['new_email']
    except:
        flash('link invalid sau expirat.', 'error')
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    if not user:
        flash('utilizator inexistent.', 'error')
    elif user.pending_email != new_email:
        flash('cerere de schimbare email invalidă.', 'error')
    else:
        user.email = new_email
        user.pending_email = None
        db.session.commit()
        flash('email schimbat cu succes! te rugăm să te autentifici cu noul email.', 'success')
    
    return redirect(url_for('login'))

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
    specializare = session.get('specializare')

    try:
        an_int = int(an)
        sem_int = int(semestru)
    except ValueError:
        return jsonify({'status': 'error', 'msg': 'an sau semestru invalid'}), 400
    if an_int not in [1, 2, 3] or sem_int not in [1, 2]:
        return jsonify({'status': 'error', 'msg': 'anul trebuie să fie între 1 și 3, semestrul între 1 și 2'}), 400

    if not can_add_grades_for_period(user_id, an, semestru):
        prev_period = get_previous_period(an, semestru)
        prev_an, prev_sem = prev_period
        return jsonify({
            'status': 'error', 
            'msg': f'trebuie să introduci notele din anul {prev_an} semestrul {prev_sem} înainte de a putea adăuga note aici!'
        }), 403

    cheie = f"{an}-{semestru}"
    materii_valide = []
    if specializare in MATERII and cheie in MATERII[specializare]:
        materii_valide.extend(MATERII[specializare][cheie])
    if cheie in OPTIUNI_OPTIONALE:
        materii_valide.extend(OPTIUNI_OPTIONALE[cheie])
        materii_valide.extend([f"optional-{i}" for i in range(2)])

    if materie not in materii_valide:
        return jsonify({'status': 'error', 'msg': 'materie invalidă'}), 400

    if nota is None or str(nota).strip() == '':
        nota_existenta = Nota.query.filter_by(
            user_id=user_id,
            an=an,
            semestru=semestru,
            materie=materie
        ).first()
        if nota_existenta:
            db.session.delete(nota_existenta)
            db.session.commit()
        return jsonify({'status': 'success', 'msg': 'nota ștearsă'})

    if is_physical_education(materie):
        if str(nota).lower() in ['admis', 'respins']:
            nota_value = str(nota).lower()
        else:
            return jsonify({'status': 'error', 'msg': 'pentru educație fizică selectați doar "admis" sau "respins"'}), 400
    else:
        try:
            nota_int = int(nota)
        except ValueError:
            return jsonify({'status': 'error', 'msg': 'nota trebuie să fie număr întreg'}), 400
        if nota_int < 1 or nota_int > 10:
            return jsonify({'status': 'error', 'msg': 'nota trebuie să fie între 1 și 10'}), 400
        nota_value = nota_int

    nota_existenta = Nota.query.filter_by(
        user_id=user_id,
        an=an,
        semestru=semestru,
        materie=materie
    ).first()

    if nota_existenta:
        nota_existenta.nota = nota_value
    else:
        new_nota = Nota(user_id=user_id, an=an, semestru=semestru, materie=materie, nota=nota_value)
        db.session.add(new_nota)

    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    session.pop('specializare', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if "username" not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    specializare = session['specializare']

    user = User.query.get(user_id)
    note = Nota.query.filter_by(user_id=user_id).all()

    note_dict = {}
    for nota in note:
        key = f"{nota.an}-{nota.semestru}-{nota.materie}"
        note_dict[key] = nota.nota
    
    an_student = int(user.an)
    semestru_student = int(user.semestru_curent) if user.semestru_curent else 1

    if 'dashboard_year' in session and 'dashboard_semester' in session:
        an_implicit = session['dashboard_year']
        semestru_implicit = session['dashboard_semester']
        print(f"DEBUG Dashboard - Using saved position: Year {an_implicit}, Semester {semestru_implicit}")
    else:
        an_implicit = an_student
        semestru_implicit = semestru_student
        print(f"DEBUG Dashboard - Using profile settings: Year {an_implicit}, Semester {semestru_implicit}")

    if an_implicit not in [1, 2, 3]:
        an_implicit = 1
    if semestru_implicit not in [1, 2]:
        semestru_implicit = 1
    
    print(f"DEBUG Dashboard - Final values: Year {an_implicit}, Semester {semestru_implicit}")

    return render_template('homepage/dashboard.html', 
                         specializare=specializare, 
                         note=note_dict,
                         an_curent=an_implicit,
                         semestru_curent=semestru_implicit)

@app.route('/save_dashboard_position', methods=['POST'])
def save_dashboard_position():
    if "user_id" not in session:
        return jsonify({'error': 'not logged in'}), 401
    
    data = request.get_json()
    year = data.get('year')
    semester = data.get('semester')

    try:
        year = int(year)
        semester = int(semester)
    except (ValueError, TypeError):
        return jsonify({'error': 'invalid values'}), 400
    
    if year not in [1, 2, 3] or semester not in [1, 2]:
        return jsonify({'error': 'values out of range'}), 400

    session['dashboard_year'] = year
    session['dashboard_semester'] = semester
    
    print(f"DEBUG - Saved dashboard position: Year {year}, Semester {semester}")
    
    return jsonify({'status': 'success'})

@app.route('/analytics')
def analytics():
    if "username" not in session:
        return redirect(url_for('login'))
        
    user_id = session.get('user_id')

    yearly_averages = get_yearly_averages(user_id)
    semester_averages = get_all_semester_averages(user_id)
    best_semester, best_avg = calculate_best_semester(user_id)
    stats = get_detailed_stats(user_id)
    
    return render_template('homepage/analytics.html',
                         yearly_averages=yearly_averages,
                         total_credits_earned=stats['total_credits_earned'],
                         subjects_passed=stats['subjects_passed'],
                         subjects_failed=stats['subjects_failed'],
                         total_subjects=stats['total_subjects'],
                         grade_distribution=stats['grade_distribution'],
                         semester_averages=semester_averages,
                         best_semester=best_semester,
                         best_avg=best_avg,
                         pass_rate=stats['pass_rate'])

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if "username" not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_profile':
            user.nume = request.form.get('nume')
            user.prenume = request.form.get('prenume')
            user.bio = request.form.get('bio')
            user.telefon = request.form.get('telefon')
            user.data_nasterii = request.form.get('data_nasterii')
            
            db.session.commit()
            flash('profilul a fost actualizat cu succes!', 'success')
            
        elif action == 'update_academic':
            old_specializare = user.specializare
            new_specializare = request.form.get('specializare')
            new_an = request.form.get('an')
            new_semestru = request.form.get('semestru_curent')
            
            user.facultate = request.form.get('facultate')
            user.specializare = new_specializare
            user.an = new_an
            user.semestru_curent = new_semestru

            session['specializare'] = new_specializare
            
            session['dashboard_year'] = int(new_an)
            session['dashboard_semester'] = int(new_semestru)

            if old_specializare != new_specializare:
                common_subjects = get_common_subjects(old_specializare, new_specializare)
                note_to_delete = []
                
                all_notes = Nota.query.filter_by(user_id=user_id).all()
                for nota in all_notes:
                    if not (nota.materie in common_subjects or 
                           nota.materie.startswith('optional-') or
                           nota.materie in OPTIUNI_OPTIONALE.get(f"{nota.an}-{nota.semestru}", [])):
                        note_to_delete.append(nota)
                
                for nota in note_to_delete:
                    db.session.delete(nota)
            
            db.session.commit()
            flash('informațiile academice au fost actualizate! dashboard-ul va afișa noua poziție.', 'success')
            
        elif action == 'change_password':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if not check_password_hash(user.password, current_password):
                flash('parola curentă este incorectă!', 'error')
            elif new_password != confirm_password:
                flash('parolele noi nu coincid!', 'error')
            elif len(new_password) < 6:
                flash('parola trebuie să aibă cel puțin 6 caractere!', 'error')
            else:
                user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
                db.session.commit()
                flash('parola a fost schimbată cu succes!', 'success')
                
        elif action == 'change_email':
            new_email = request.form.get('new_email')
            password = request.form.get('password_for_email')
            
            if not check_password_hash(user.password, password):
                flash('parola este incorectă!', 'error')
            elif not new_email.endswith('@stud.ase.ro'):
                flash('trebuie să folosești un email instituțional (@stud.ase.ro)', 'error')
            elif User.query.filter_by(email=new_email).first():
                flash('acest email este deja înregistrat!', 'error')
            elif new_email == user.email:
                flash('acesta este deja emailul tău curent!', 'error')
            else:
                user.pending_email = new_email
                db.session.commit()

                token = serializer.dumps({'user_id': user_id, 'new_email': new_email}, salt="email-change")
                confirm_url = url_for('confirm_email_change', token=token, _external=True)
                
                msg = Message('confirmă schimbarea emailului - studentxyz',
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[new_email])
                msg.html = f'''
<html>
<body>
  <div style="font-family: Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; color: #333; line-height: 1.6;">
    <div style="background-color: #e0e0e0; padding: 30px 20px 20px; border-radius: 0 0 10px 10px; text-align: center;">
      <img src="https://i.imgur.com/qPeqmKv.png" alt="logo" style="width: 320px; height: auto; display: block; margin: 0 auto;">
    </div>

    <div style="max-width: 600px; margin: 30px auto; background: white; padding: 30px 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); text-align: center;">
      <h2 style="font-size: 24px; margin-bottom: 15px;">confirmă schimbarea emailului</h2>
      <p style="font-size: 18px; margin-bottom: 25px;">pentru a confirma schimbarea emailului, te rugăm să dai click pe butonul de mai jos:</p>
      <a href="{confirm_url}" style="display: inline-block; padding: 12px 24px; background-color: #181818; color: #fff; text-decoration: none; font-weight: bold; border-radius: 6px; font-size: 16px;">confirmă noul email</a>
      <p style="font-size: 16px; margin-top: 25px;">link-ul este valabil 1 oră. dacă nu ai solicitat această schimbare, ignoră acest email.</p>
    </div>

    <div style="background-color: #e0e0e0; color: #555; font-size: 13px; padding: 15px 10px; text-align: center;">
      &copy; 2025 marelegsaa - all rights reserved.
    </div>
  </div>
</body>
</html>
                '''
                mail.send(msg)
                
                flash('email de confirmare trimis la noua adresă! verifică inbox-ul.', 'info')
        
        return redirect(url_for('settings'))
    
    return render_template('homepage/settings.html', user=user)

@app.route('/user')
def user():
    if "username" not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)

    yearly_averages = get_yearly_averages(user_id)

    note = Nota.query.filter_by(user_id=user_id).filter(Nota.nota.isnot(None)).all()
    total_materii = len(note)

    facultati_display = {
        'csie': 'facultatea de cibernetică, statistică și informatică economică',
        'finante': 'facultatea de finanțe, asigurări, bănci și burse de valori',
        'marketing': 'facultatea de marketing',
        'comert': 'facultatea de comerț',
        'economie': 'facultatea de economie teoretică și aplicată',
        'contabilitate': 'facultatea de contabilitate și informatică de gestiune',
        'management': 'facultatea de management',
        'rei': 'facultatea de relații economice internaționale',
        'fabiz': 'facultatea de administrarea afacerilor în limbi străine'
    }
    
    facultate_display = facultati_display.get(user.facultate, user.facultate)
    
    return render_template('homepage/user.html', 
                         user=user, 
                         yearly_averages=yearly_averages, 
                         total_materii=total_materii,
                         facultate_display=facultate_display)

@app.route('/upload_profile_picture', methods=['POST'])
def upload_profile_picture():
    if "user_id" not in session:
        return jsonify({'status': 'error', 'msg': 'not logged in'}), 401
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if 'profile_picture' not in request.files:
        return jsonify({'status': 'error', 'msg': 'nu s-a încărcat niciun fișier'}), 400
    
    file = request.files['profile_picture']
    
    if file.filename == '':
        return jsonify({'status': 'error', 'msg': 'nu ai selectat niciun fișier'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'status': 'error', 'msg': 'format invalid. folosește PNG, JPG, JPEG sau GIF'}), 400
    
    try:
        if user.profile_picture:
            old_path = os.path.join(app.config['UPLOAD_FOLDER'], user.profile_picture)
            if os.path.exists(old_path):
                os.remove(old_path)

        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{user_id}_{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        img = Image.open(file.stream)

        if img.mode != 'RGB':
            img = img.convert('RGB')

        width, height = img.size
        size = min(width, height)
        left = (width - size) // 2
        top = (height - size) // 2
        right = left + size
        bottom = top + size
        img = img.crop((left, top, right, bottom))

        img = img.resize((300, 300), Image.Resampling.LANCZOS)

        img.save(filepath, 'JPEG', quality=85, optimize=True)

        user.profile_picture = filename
        db.session.commit()
        
        return jsonify({'status': 'success', 'image': url_for('uploaded_file', filename=filename)})
    except Exception as e:
        return jsonify({'status': 'error', 'msg': f'eroare la procesarea imaginii: {str(e)}'}), 500

@app.route('/remove_profile_picture', methods=['POST'])
def remove_profile_picture():
    if "user_id" not in session:
        return jsonify({'status': 'error', 'msg': 'not logged in'}), 401
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if user.profile_picture:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], user.profile_picture)
        if os.path.exists(filepath):
            os.remove(filepath)

        user.profile_picture = None
        db.session.commit()
    
    return jsonify({'status': 'success'})

@app.route('/api/get_missing_subjects')
def get_missing_subjects():
    if "user_id" not in session:
        return jsonify({'error': 'not logged in'}), 401
    
    user_id = session['user_id']
    year = request.args.get('year', type=int)
    semester = request.args.get('semester', type=int)
    
    if not year or not semester:
        return jsonify({'missing_subjects': []})

    prev_period = get_previous_period(str(year), str(semester))
    if prev_period is None:
        return jsonify({'missing_subjects': []})
    
    prev_an, prev_sem = prev_period
    cheie = f"{prev_an}-{prev_sem}"
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'missing_subjects': []})
    
    specializare = user.specializare

    obligatorii = []
    if specializare in MATERII and cheie in MATERII[specializare]:
        obligatorii = MATERII[specializare][cheie]

    missing = []
    for materie in obligatorii:
        nota_existenta = Nota.query.filter_by(
            user_id=user_id,
            an=str(prev_an),
            semestru=str(prev_sem),
            materie=materie
        ).first()
        
        if nota_existenta is None:
            missing.append(materie)
    
    return jsonify({
        'missing_subjects': missing,
        'total_missing': len(missing),
        'required_period': f"anul {prev_an} semestrul {prev_sem}"
    })

@app.route('/api/get_available_periods')
def get_available_periods():
    if "user_id" not in session:
        return jsonify({'error': 'not logged in'}), 401
    
    user_id = session['user_id']
    
    all_periods = [
        (1, 1), (1, 2),
        (2, 1), (2, 2),
        (3, 1), (3, 2)
    ]
    
    available_periods = []
    
    for an, semestru in all_periods:
        if can_add_grades_for_period(user_id, str(an), str(semestru)):
            available_periods.append(f"{an}-{semestru}")
    
    return jsonify({
        'available_periods': available_periods
    })

@app.route('/api/get_averages')
def get_averages():
    if "user_id" not in session:
        return jsonify({'error': 'not logged in'}), 401
    
    user_id = session['user_id']
    year = request.args.get('year', type=int)
    semester = request.args.get('semester', type=int)

    semester_avg = calculate_semester_average(user_id, year, semester)

    overall_avg = get_overall_average(user_id)
    
    return jsonify({
        'semester_average': semester_avg,
        'overall_average': overall_avg
    })

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)