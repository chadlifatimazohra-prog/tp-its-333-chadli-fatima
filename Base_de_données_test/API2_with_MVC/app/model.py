DB_NAME = "database.db"

def init_db():
    with sqlite3.connect(DB_NAME) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS etudiants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                addr TEXT,
                pin TEXT
            )
        """)
        con.commit()

def ajouter_etudiant(nom, addr, pin):
    with sqlite3.connect(DB_NAME) as con:
        con.execute(
            "INSERT INTO etudiants (nom, addr, pin) VALUES (?, ?, ?)",
            (nom, addr, pin)
        )
        con.commit()

def get_etudiants():
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.execute("SELECT id, nom, addr, pin FROM etudiants")
        return cur.fetchall()

def update_etudiant(id, addr, pin):
    with sqlite3.connect(DB_NAME) as con:
        con.execute(
            "UPDATE etudiants SET addr=?, pin=? WHERE id=?",
            (addr, pin, id)
        )


