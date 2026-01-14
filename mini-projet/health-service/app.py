from flask import Flask, request, jsonify
import json
import os
import requests
from flask_cors import CORS
import jwt
from functools import wraps

app = Flask(__name__)
CORS(app)

DATA_FILE = 'data.json'
PERSON_SERVICE_URL = os.environ.get('PERSON_URL', "http://127.0.0.1:5001/persons/")
SECRET_KEY = "super_secret_key_microservices"

def load_data():
    if not os.path.exists(DATA_FILE): return {}
    with open(DATA_FILE, 'r') as f:
        try: return json.load(f)
        except: return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f: json.dump(data, f, indent=4)

def check_person_exists(person_id):
    try:
        response = requests.get(f"{PERSON_SERVICE_URL}{person_id}")
        return response.status_code == 200
    except: return False

# --- LE VIGILE ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token manquant !'}), 401
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token invalide !'}), 401
        return f(*args, **kwargs)
    return decorated

# --- ROUTES ---

@app.route('/health/<person_id>', methods=['POST'])
@token_required # <--- SÉCURISÉ
def add_health_data(person_id):
    if not check_person_exists(person_id):
        return jsonify({"error": "Cette personne n'existe pas !"}), 404
    content = request.json
    data = load_data()
    data[str(person_id)] = content
    save_data(data)
    return jsonify({"message": "Données enregistrées", "data": content}), 201

@app.route('/health/<person_id>', methods=['GET'])
# Lecture publique (pas de token)
def get_health_data(person_id):
    if not check_person_exists(person_id): return jsonify({"error": "Inconnu"}), 404
    data = load_data()
    return jsonify(data.get(str(person_id)) or {"message": "Pas de données"}), 200 if str(person_id) in data else 404

@app.route('/health/<person_id>', methods=['DELETE'])
@token_required # <--- SÉCURISÉ
def delete_health_data(person_id):
    data = load_data()
    if str(person_id) in data:
        del data[str(person_id)]
        save_data(data)
        return jsonify({"message": "Données supprimées"}), 200
    return jsonify({"error": "Pas de données"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)