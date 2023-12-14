import shutil

from flask import Flask, render_template, request
import os
import backend as bk
from collections import OrderedDict
def vider_dossier(dossier):
    # Vérifier si le dossier existe
    if os.path.exists(dossier):
        # Parcourir tous les fichiers et sous-dossiers du dossier
        for fichier in os.listdir(dossier):
            chemin_fichier = os.path.join(dossier, fichier)

            # Vérifier si c'est un fichier
            if os.path.isfile(chemin_fichier):
                # Supprimer le fichier
                os.remove(chemin_fichier)
            elif os.path.isdir(chemin_fichier):
                # Si c'est un sous-dossier, appeler la fonction récursivement
                vider_dossier(chemin_fichier)

    else:
        print(f"Le dossier '{dossier}' n'existe pas.")

def copier_contenu_dossier(source, destination):
    try:
        # Vérifier si le dossier de destination existe
        if not os.path.exists(destination):
            os.makedirs(destination)  # Créer le dossier de destination s'il n'existe pas

        # Copier le contenu du dossier source vers le dossier destination
        for item in os.listdir(source):
            s = os.path.join(source, item)
            d = os.path.join(destination, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks=True, ignore=None)
            else:
                shutil.copy2(s, d)
        print(f"Contenu de '{source}' copié avec succès vers '{destination}'.")
    except Exception as e:
        print(f"Erreur lors de la copie du contenu de '{source}' vers '{destination}': {e}")


# copier_contenu_dossier("downloads", "static")

app = Flask(__name__)

# Route pour afficher la page d'accueil
@app.route('/')
def home():
    return render_template('index.html')
    # return 'Hello, World!'
@app.route('/describe')
def describe():
    dictionnaire_modifie = {cle: valeur.strip('[]').strip('"') for cle, valeur in bk.infocv().items()}
    dictionnaire_modifie.pop('Picture', None)

    return  render_template('resultat.html', data=dictionnaire_modifie)


# Route pour traiter le téléchargement du fichier
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    # Vérifiez si le dossier "uploads" existe, sinon, créez-le
    upload_folder = 'uploads'
    vider_dossier(upload_folder)
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Enregistrez le fichier dans le dossier "uploads"
    file.save(os.path.join(upload_folder, file.filename))
    path=upload_folder +'/'+file.filename
    # print(path)
    vider_dossier("static")
    bk.predir(path)
    # print(bk.infocv())
    # Afficher les résultats optimisés

    # for key, text in bk.infocv().items():
    #     print(f'"{key}": {text}\n')

    dictionnaire_modifie = {cle: valeur.strip('[]').strip('"') for cle, valeur in bk.infocv().items()}

    parent_folder_path = 'static/predict/crops'
    result_dict = bk.build_image_dictionary(parent_folder_path)
    # return  render_template('resultat.html', data=dictionnaire_modifie)
    return render_template('listerImg.html', data=result_dict)

# @app.route('/result')
# def resultat():
#     exemple_data = bk.infocv()
#     return render_template('resultat.html', data=exemple_data)



if __name__ == '__main__':
    app.run(debug=True)
