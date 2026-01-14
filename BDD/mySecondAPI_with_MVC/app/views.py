from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Création de la base
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute("""
        CREATE TABLE IF NOT EXISTS etudiants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            adress TEXT,
            pincode TEXT
        )
    """)
    conn.close()

init_db()

# Page formulaire
@app.route('/')
def index():
    return render_template('form.html')

# Ajout étudiant
@app.route('/new', methods=['POST'])
def add_etudiant():
    nom = request.form['nom']
    adress = request.form['adress']
    pincode = request.form['pincode']

    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO etudiants (nom, adress, pincode) VALUES (?, ?, ?)",
            (nom, adress, pincode)
        )
        con.commit()

    # 🔁 Redirection vers le tableau
    return redirect(url_for('liste_etudiants'))

# Afficher les étudiants en TABLEAU HTML
@app.route('/etudiants')
def liste_etudiants():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT nom, adress, pincode FROM etudiants")
    rows = cur.fetchall()
    conn.close()

    return render_template("base.html", etudiants=rows)

if __name__ == '__main__':
    app.run(debug=True)
