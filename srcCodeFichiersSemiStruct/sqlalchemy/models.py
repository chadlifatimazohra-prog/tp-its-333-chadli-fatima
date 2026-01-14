from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Groupe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)
    etudiants = db.relationship('Etudiant', backref='groupe')

class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), unique=True, nullable=False)
    adresse = db.Column(db.String(120), nullable=False)
    pin = db.Column(db.String(20), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groupe.id'))

def init_db():
    with app.app_context():
        db.create_all()