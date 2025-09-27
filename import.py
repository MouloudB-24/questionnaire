import requests
import json
import unicodedata
from pathlib import Path

# ====> REMARQUE : Les Url ci-dessous sont différentes que celles affichées dans la vidéo.
# C'est normal, continuez bien avec les url de ce fichier
open_quizz_db_data = (
    ("Animaux", "Les chats", "https://www.codeavecjonathan.com/res/mission/openquizzdb_50.json"),
    ("Arts", "Musée du Louvre", "https://www.codeavecjonathan.com/res/mission/openquizzdb_86.json"),
    ("Bande dessinnée", "Tintin", "https://www.kiwime.com/oqdb/files/2124627384/OpenQuizzDB_124/openquizzdb_124.json"),
    ("Cinéma", "Alien", "https://www.codeavecjonathan.com/res/mission/openquizzdb_241.json"),
    ("Cinéma", "Star wars", "https://www.codeavecjonathan.com/res/mission/openquizzdb_90.json"),
)


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def get_quizz_filename(categorie, titre, difficulte):
    return strip_accents(categorie).lower().replace(" ", "") + "_" + strip_accents(titre).lower().replace(" ", "") + "_" + strip_accents(difficulte).lower().replace(" ", "") + ".json"


def generate_json_file(categorie, titre, url):
    out_questionnaire_data = {"categorie": categorie, "titre": titre, "questions": []}
    out_questions_data = []
    
    # Faire le requete url
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Request failed with status code: {response.status_code}")
        return
    try:
        data = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        print(f"No valid JSON from the url: {url}")
        return
    all_quizz = data["quizz"]["fr"]
    
    for quizz_title, quizz_data in all_quizz.items():
        out_filename = get_quizz_filename(categorie, titre, quizz_title)
        out_questionnaire_data["difficulte"] = quizz_title
        for question in quizz_data:
            question_dict = {}
            question_dict["titre"] = question["question"]
            question_dict["choix"] = []
            for ch in question["propositions"]:
                question_dict["choix"].append((ch, ch==question["réponse"]))
            out_questions_data.append(question_dict)
        out_questionnaire_data["questions"] = out_questions_data
        out_json = json.dumps(out_questionnaire_data, indent=4)

        data_folder =  Path("data")
        data_folder.mkdir(exist_ok=True)
        with open((data_folder / out_filename), "w", encoding="utf-8") as f:
            f.write(out_json)       
        print("End")


if __name__ == "__main__":
    for quizz_data in open_quizz_db_data:
        generate_json_file(quizz_data[0], quizz_data[1], quizz_data[2])

