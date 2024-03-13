from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient(
    "mongodb+srv://elouafimed2:gXeAq06sbLpRa8o2@cluster0.tptk8nt.mongodb.net/test?retryWrites=true&w=majority&appName=Cluster0"
)
db = client.quiz2database  # Remplacez "test" par le nom de votre base de données

app = Flask(__name__)
CORS(app)


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # Rechercher l'utilisateur dans la base de données
    utilisateur = db.user.find_one(
        {"email": email, "password": password}
    )  # Assurez-vous que "utilisateurs" est le nom de votre collection

    # Vérifier si l'utilisateur existe
    if utilisateur:
        return jsonify({"message": "oui"}), 200
    else:
        return jsonify({"message": "non"}), 404


@app.route("/ajouter_utilisateur", methods=["POST"])
def ajouter_utilisateur():
    data = request.json
    print(data.get("nom"))
    utilisateur = {
        "id": "50",
        "nom": data.get("nom"),
        "email": data.get("email"),
        "password": data.get("password"),
    }
    # Insérer l'utilisateur dans la base de données
    db.user.insert_one(
        utilisateur
    )  # Assurez-vous que "utilisateurs" est le nom de votre collection
    return jsonify({"message": "Utilisateur ajouté avec succès"}), 201


@app.route("/ajouter_utilisateur2", methods=["GET"])
def add_user_get():
    utilisateur = {
        "id": "2",
        "nom": "med",
        "email": "elouafimed2@gmail.com",
        "password": "1234",
    }
    # Insérer l'utilisateur dans la base de données
    db.user.insert_one(
        utilisateur
    )  # Assurez-vous que "utilisateurs" est le nom de votre collection
    return jsonify({"message": "Utilisateur ajouté avec succès"}), 201


@app.route("/startquiz", methods=["GET"])
def start_quiz():
    questions = {
        "Quel langage de programmation est souvent utilisé pour le développement web?": {
            "a": "Python",
            "b": "JavaScript",
            "c": "C#",
            "correct": "b",
        },
        "Qu'est-ce qu'une boucle 'for' dans la plupart des langages de programmation?": {
            "a": "Une structure de contrôle utilisée pour exécuter un bloc de code un nombre fixe de fois",
            "b": "Une méthode pour déclarer des variables",
            "c": "Une instruction pour terminer prématurément l'exécution d'un programme",
            "correct": "a",
        },
        "Quel est le principal avantage de l'utilisation des fonctions dans la programmation?": {
            "a": "Réduire la lisibilité du code",
            "b": "Faciliter le débogage et la réutilisation du code",
            "c": "Ralentir l'exécution du programme",
            "correct": "b",
        },
        "Que signifie l'acronyme 'API' dans le contexte de la programmation?": {
            "a": "Application Program Instruction",
            "b": "Automated Programming Interface",
            "c": "Application Programming Interface",
            "correct": "c",
        },
        "Quel est le rôle principal d'un serveur dans une architecture client-serveur?": {
            "a": "Gérer l'interface utilisateur",
            "b": "Fournir des ressources et des services aux clients",
            "c": "Interpréter le code source",
            "correct": "b",
        },
    }
    # Correction de la méthode pour renvoyer le contenu JSON avec le code de statut 200
    return jsonify({"message": "ok", "quiz": questions}), 200


@app.route("/score", methods=["GET"])
def score():
    data = request.get_json()
    array1 = data[0]
    corecteReponce = ["b", "a", "b", "c", "b"]
    return jsonify({"message": "ok", "corecteReponce": corecteReponce}), 201


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
