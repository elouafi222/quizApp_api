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
        profession = utilisateur.get("fonctionaliter", "")
        return jsonify({"message": "teacher"}), 200
    elif db.student.find_one({"email": email, "password": password}):
        return jsonify({"message": "student"}), 200
    else:
        return jsonify({"message": "non"}), 404


@app.route("/ajouter_utilisateur", methods=["POST"])
def ajouter_utilisateur():
    data = request.json
    print(data.get("nom"))

    email_existant = db.user.find_one(
        {"email": data.get("email")}
    ) or db.student.find_one({"email": data.get("email")})
    if email_existant:
        # Si un utilisateur avec le même email existe déjà, renvoyer une erreur
        return jsonify({"message": "emailExiste"}), 201

    if data.get("fonctionaliter") != "student":
        utilisateur = {
            "nom": data.get("nom"),
            "email": data.get("email"),
            "password": data.get("password"),
            "quiz": [],
        }

        # Insérer l'utilisateur dans la collection "user" ou "student" en fonction de sa fonctionalité
        db.user.insert_one(utilisateur)
    else:
        student = {
            "nom": data.get("nom"),
            "email": data.get("email"),
            "password": data.get("password"),
            "quizpasse": [],
        }

        db.student.insert_one(student)

    return jsonify({"message": "ok"}), 201


@app.route("/createquiz", methods=["POST"])
def ajouter_quiz():
    data = request.json
    print(data.get("emailteacher"))

    email = data.get("emailteacher")

    if email == "":
        return jsonify({"message": "problemeemail"}), 404

    else:
        utilisateur = db.user.find_one({"email": email})
        # Vérifiez si l'utilisateur existe
        if utilisateur:
            # Récupérez l'ID de l'utilisateur
            user_id = utilisateur["_id"]

            quiz = {
                "quizname": data.get("quizname"),
                "description": data.get("description"),
                "codequiz": data.get("codequiz"),
                "idcreateur": user_id,
                "question": [],
            }
            # Insérer le quiz dans la collection "quiz"
            result = db.quiz.insert_one(quiz)

            # Récupérer l'ID du quiz créé
            quiz_id = result.inserted_id

            # Mettre à jour la collection des quizzes de l'utilisateur
            db.user.update_one({"_id": user_id}, {"$push": {"quiz": quiz_id}})

            return jsonify({"message": "quizcreer"}), 201

        else:
            return jsonify({"message": "usernotexiste"}), 404


@app.route("/recupererAllQuiz", methods=["POST"])
def recuper_allquiz():
    data = request.json
    # data = dataArray[0]
    print(data.get("emailteacher"))

    email = data.get("emailteacher")

    if email == "":
        return jsonify({"message": "problemeemail"}), 404

    else:
        utilisateur = db.user.find_one({"email": email})
        # Vérifiez si l'utilisateur existe
        if utilisateur:
            # Récupérez l'ID de l'utilisateur
            user_id = utilisateur["_id"]

            # Recherchez tous les quizzes créés par cet utilisateur
            quizzes_utilisateur = db.quiz.find({"idcreateur": user_id})

            # Convertissez le curseur en une liste de dictionnaires
            quizzes = []
            for quiz in quizzes_utilisateur:
                # Convertir l'ObjectId en chaîne de caractères
                quizzes.append(
                    {
                        "quizname": quiz["quizname"],
                        "description": quiz["description"],
                        "codequiz": quiz["codequiz"],
                        # Ajoutez d'autres informations de quiz si nécessaire
                    }
                )

            return jsonify({"quizzes": quizzes}), 200

        else:
            return jsonify({"message": "usernotexiste"}), 404


@app.route("/createquestion", methods=["POST"])
def ajouter_question():
    data = request.json
    print(data.get("email"))

    email = data.get("email")

    if email == "":
        return jsonify({"message": "problemeemail"}), 404

    else:
        utilisateur = db.user.find_one({"email": email})

        # Vérifiez si l'utilisateur existe
        if utilisateur:
            # Récupérez l'ID de l'utilisateur
            user_id = utilisateur["_id"]

            quiz = db.quiz.find_one(
                {"quizname": data.get("quizname"), "idcreateur": user_id}
            )

            quiz_id = quiz["_id"]
            question = {
                "question": data.get("question"),
                "reponcea": data.get("reponcea"),
                "reponceb": data.get("reponceb"),
                "reponcec": data.get("reponcec"),
                "reponcecorecte": data.get("reponcecorecte"),
                "quizid": quiz_id,
            }
            # Insérer le quiz dans la collection "question"
            result = db.question.insert_one(question)

            # Récupérer l'ID du quiz créé
            question_id = result.inserted_id

            # Mettre à jour la collection des question pour les quiz
            db.quiz.update_one({"_id": quiz_id}, {"$push": {"question": question_id}})

            return jsonify({"message": "questioncreer"}), 201

        else:
            return jsonify({"message": "usernotexiste"}), 404


@app.route("/recupererAllQuestion", methods=["POST"])
def recuper_allquestion():
    data = request.json
    # data = dataArray[0]
    print(data.get("emailteacher"))
    print(data.get("quizname"))

    email = data.get("emailteacher")
    quizname = data.get("quizname")

    if email == "":
        return jsonify({"message": "problemeemail"}), 404

    else:
        utilisateur = db.user.find_one({"email": email})
        # Vérifiez si l'utilisateur existe
        if utilisateur:
            # Récupérez l'ID de l'utilisateur
            user_id = utilisateur["_id"]
            print("userid ", user_id)

            quiz = db.quiz.find_one(
                {"quizname": data.get("quizname"), "idcreateur": user_id}
            )
            quiz_id = quiz["_id"]
            print("quiz_id", quiz_id)

            # Recherchez tous les quizzes créés par cet utilisateur
            question_utilisateur = db.question.find({"quizid": quiz_id})

            # Convertissez le curseur en une liste de dictionnaires
            questions = []
            for question in question_utilisateur:
                # Convertir l'ObjectId en chaîne de caractères
                print(question)
                questions.append(
                    {
                        "question": question["question"],
                        "reponcea": question["reponcea"],
                        "reponceb": question["reponceb"],
                        "reponcec": question["reponcec"],
                        "reponcecorecte": question["reponcecorecte"],
                        # Ajoutez d'autres informations de quiz si nécessaire
                    }
                )
            print((questions))
            return jsonify({"questions": questions}), 200

        else:
            return jsonify({"message": "usernotexiste"}), 404


@app.route("/ajouter_utilisateur2", methods=["GET"])
def add_user_get():
    utilisateur = {
        "nom": "med",
        "email": "elouafimed2@gmail.com",
        "password": "1234",
        "fonctionaliter": "student",
    }
    # Insérer l'utilisateur dans la base de données
    db.user.insert_one(
        utilisateur
    )  # Assurez-vous que "utilisateurs" est le nom de votre collection
    return jsonify({"message": "Utilisateur ajouté avec succès"}), 201


@app.route("/ratequiz", methods=["POST"])
def start_quiz():
    data = request.json
    code_quiz = data["codequiz"]
    emailprof = data["emailprof"]
    emailstudent = data["emailstudent"]
    localisation = data["localisation"]
    score = data["score"]

    prof = db.user.find_one({"email": emailprof})
    student = db.student.find_one({"email": emailstudent})
    if prof:

        quiz = db.quiz.find_one({"codequiz": code_quiz, "idcreateur": prof["_id"]})
        if quiz:

            quipasse = db.quizpasse.find_one(
                {"id_student": student["_id"], "id_quiz": quiz["_id"]}
            )

            if quipasse:
                db.quizpasse.update_one(
                    {"_id": quipasse["_id"]},
                    {"$push": {"score": score, "localisation": localisation}},
                )
            else:
                Quizpass = {
                    "id_student": student["_id"],
                    "id_quiz": quiz["_id"],
                    "localisation": localisation,
                    "score": score,
                }
                db.quizpasse.insert_one(Quizpass)

                # Correction de la méthode pour renvoyer le contenu JSON avec le code de statut 200
                return jsonify({"quiz": "quizrate"}), 200

        else:
            return jsonify({"message": "quiznotexiste"}), 404
    else:
        return jsonify({"message": "usernotexiste"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
