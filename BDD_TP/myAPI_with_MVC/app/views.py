from app import app
from flask import render_template, request
import sqlite3

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nom = request.form['nom']
        addr = request.form['addr']
        pin = request.form['pin']

        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS etudiants (
                    nom TEXT,
                    addr TEXT,
                    pin TEXT
                )
            """)
            cur.execute(
                "INSERT INTO etudiants (nom, addr, pin) VALUES (?, ?, ?)",
                (nom, addr, pin)
            )
            con.commit()

        return "Étudiant ajouté avec succès"

    return render_template("index.html")


@app.route('/list')
def list_students():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT rowid, nom, addr, pin FROM etudiants")
    students = cur.fetchall()
    con.close()

    return render_template("list.html", students=students)