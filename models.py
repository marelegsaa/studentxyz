from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(100), nullable=False)
    prenume = db.Column(db.String(100), nullable=False)
    facultate = db.Column(db.String(100), nullable=False)
    specializare = db.Column(db.String(100), nullable=False)
    an = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    an = db.Column(db.Integer, nullable=False)
    semestru = db.Column(db.Integer, nullable=False)
    materie = db.Column(db.String(120), nullable=False)
    nota = db.Column(db.Integer, nullable=True)

    user = db.relationship('User', backref=db.backref('note', lazy=True))
