from models import db, Etudiant, Groupe, app

with app.app_context():

    # Créer la base (si pas déjà faite)
    db.create_all()

    # Créer un groupe ITS2
    its2 = Groupe(nom='ITS2')
    db.session.add(its2)
    db.session.commit()

    # Créer 3 étudiants avec le style donné
    Fatima = Etudiant(nom='Fatima', adresse='paris', pin='034', groupe=its2)
    Isabelle = Etudiant(nom='Isabelle', adresse='rue Paris', pin='075', groupe=its2)
    Elveda = Etudiant(nom='Elveda', adresse='rue Isparta', pin='032', groupe=its2)

    db.session.add_all([Fatima, Isabelle, Elveda])
    db.session.commit()

    # Afficher pour vérifier
    print(Etudiant.query.all())