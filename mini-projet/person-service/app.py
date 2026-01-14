from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import requests  # Nécessaire pour appeler le service santé
import jwt
from functools import wraps

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_KEY = "super_secret_key_microservices"

# Adresse du Service Santé (Variable d'environnement Docker ou par défaut localhost)
HEALTH_SERVICE_URL = os.environ.get('HEALTH_URL', "http://127.0.0.1:5002/health/")

db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def to_dict(self): return {"id": self.id, "name": self.name}


with app.app_context():
    db.create_all()


# --- VIGILE (Token) ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token: return jsonify({'message': 'Token manquant !'}), 401
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token invalide !'}), 401
        return f(*args, **kwargs)

    return decorated


# --- ROUTES ---

# 1. NOUVEAU : Récupérer TOUTE la liste
@app.route('/persons', methods=['GET'])
def get_all_persons():
    persons = Person.query.all()
    # On renvoie une liste JSON : [{"id":1, "name":"..."}, ...]
    return jsonify([p.to_dict() for p in persons]), 200


@app.route('/persons', methods=['POST'])
@token_required
def create_person():
    data = request.json
    if not data or 'name' not in data: return jsonify({"error": "Nom manquant"}), 400
    new_person = Person(name=data['name'])
    db.session.add(new_person)
    db.session.commit()
    return jsonify(new_person.to_dict()), 201


# --- AJOUTE CECI ---
@app.route('/persons/<int:id>', methods=['GET'])
def get_person(id):
    person = Person.query.get(id)
    if person:
        return jsonify(person.to_dict()), 200
    return jsonify({"error": "Personne introuvable"}), 404


# -------------------
@app.route('/persons/<int:id>', methods=['DELETE'])
@token_required
def delete_person(id):
    person = Person.query.get(id)
    if person:
        # 1. On supprime la personne de la base locale (Service Personne)
        db.session.delete(person)
        db.session.commit()

        # 2. INTELLIGENCE : On appelle le Service Santé pour nettoyer aussi !
        # On essaie, mais si le service santé est éteint, on ne fait pas planter le tout
        try:
            # On envoie le token aussi pour avoir le droit de supprimer là-bas
            headers = {'x-access-token': request.headers.get('x-access-token')}
            requests.delete(f"{HEALTH_SERVICE_URL}{id}", headers=headers, timeout=2)
            msg_sante = " + Dossier médical supprimé."
        except:
            msg_sante = " (Mais impossible de joindre le service santé)."

        return jsonify({"message": f"Personne supprimée{msg_sante}"}), 200

    return jsonify({"error": "Personne introuvable"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)