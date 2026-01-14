from flask import render_template_string
from models import app, db, Groupe

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    groupe = Groupe.query.filter_by(nom='ITS2').first()
    return render_template_string("""
    <h1>Groupe {{ groupe.nom }}</h1>
    <ul>
    {% for e in groupe.etudiants %}
        <li>{{ e.nom }} - {{ e.adresse }} - {{ e.pin }}</li>
    {% endfor %}
    </ul>
    """, groupe=groupe)

if __name__ == '__main__':
    app.run(debug=True)