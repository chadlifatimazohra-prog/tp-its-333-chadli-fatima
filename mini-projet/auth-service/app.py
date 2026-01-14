from flask import Flask, request, jsonify
import jwt
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SECRET_KEY = "super_secret_key_microservices"


@app.route('/login', methods=['POST'])
def login():
    data = request.json

    if data and data.get('username') == "admin" and data.get('password') == "admin":
        token = jwt.encode({
            'user': 'admin',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({'token': token})

    return jsonify({'message': 'Mauvais login/mot de passe !'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)