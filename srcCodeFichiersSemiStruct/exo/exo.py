import json

# Charger le fichier JSON
with open("exo.json", "r") as f:
    personnes = json.load(f)

def chercher_parametres_sante(id_personne):
    if id_personne in personnes:
        return json.dumps(personnes[id_personne], indent=4)
    else:
        return json.dumps({"erreur": "Personne non trouvée"}, indent=4)

# Test avec ID existant
print(chercher_parametres_sante("3"))
