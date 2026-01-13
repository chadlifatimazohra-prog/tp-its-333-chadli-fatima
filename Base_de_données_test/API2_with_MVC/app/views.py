from app import app
from flask import render_template, request, redirect
import sqlite3
from .database import init_db

init_db()

@app.route('/')
def home():
    return redirect('/new')

@app.route('/new')
def new():
    return render_template("new.html")

@app.route('/new', methods=['POST'])
def add_patient():
    nom = request.form['nom']
    adresse = request.form['adresse']
    pin = request.form['pin']

    conn = sqlite3.connect("sante.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO patients (nom, adresse, pin) VALUES (?,?,?)",
                (nom, adresse, pin))
    conn.commit()
    conn.close()

    return redirect('/list')

@app.route('/list')
def list_patients():
    conn = sqlite3.connect("sante.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    data = cur.fetchall()
    conn.close()

    return render_template("list.html", patients=data)

