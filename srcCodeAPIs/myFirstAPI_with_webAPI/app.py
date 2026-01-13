from flask import Flask, jsonify, request

app = Flask(__name__)




## EXO1: API GET - Hello World
@app.route('/api/salutation', methods=['GET'])
def salutation():
    return jsonify(message="Hello World")

## EXO2: API POST - renvoyer un nom fourni en paramètre
@app.route('/api/utilisateurs', methods=['GET', 'POST'])
def creer_utilisateur():
    data = request.get_json()

    # Vérification simple
    if not data or 'nom' not in data:
        return jsonify(error="Paramètre 'nom' manquant"), 400

    nom = data['nom']
    return jsonify(message=f"Bonjour {nom}")


# to be tested with curl:
# >> curl -i -X GET http://localhost:5000/api/salutation
# >> curl -i -X POST -H 'Content-Type: application/json' -d '{"nom": "Bob"}' http://localhost:5000/api/utilisateurs