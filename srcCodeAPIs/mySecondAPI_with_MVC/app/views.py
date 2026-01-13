from app import app

from flask import render_template, request, jsonify

### EXO1 - simple API

@app.route('/route1')
def index():
    return "hello world"

### EXO2 - API with simple display

@app.route('/route2')
def index():
    return  render_template('index.html')

### EXO3 - API with parameters display



### EXO4 - API with parameters retrieved from URL

@app.route('/params', methods=['GET'])
def params():
    surname = request.args.get('surname')
    name = request.args.get('name')
    return f"{name} {surname}"

# commande bash : curl "http://127.0.0.1:5000/params?surname=Dupont&name=Jean"

if __name__ == '__main__':
    app.run(debug=True)
