import pytesseract
import os
from IPython.display import Image
from ultralytics import YOLO
from PIL import Image

import cv2
from pdf2image import convert_from_path
import numpy as np



def convert_pdf_to_image(pdf_path, output_format='JPEG'):
    images = convert_from_path(pdf_path, fmt=output_format)

    # Vérifier si des static ont été extraites
    if images:
        # Convertir la première image en tableau Numpy
        img = np.array(images[0])

        # Pour chaque image supplémentaire, concaténer le tableau Numpy
        for i in range(1, len(images)):
            img = np.concatenate((img, np.array(images[i])), axis=1)

        return img

    return None


# def redimensionner_image(image, nouvelle_taille):
#     # Redimensionner l'image avec anti-aliasing (par défaut)
#     img_redimensionnee = image.resize((nouvelle_taille, nouvelle_taille))
#
#     return img_redimensionnee

def predir(image_path):
    try:
        if image_path.lower().endswith('.pdf'):
            image = convert_pdf_to_image(image_path)

            # Assurez-vous que la conversion en tableau Numpy a réussi
            if image is not None:
                # Convertir l'image PIL en tableau NumPy
                r = np.array(image)

            model = YOLO("runs/detect/train5/weights/best.pt")
            model.predict(r, save=True, save_crop=True, classes=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],project="static", exist_ok=True)
        else:
            # Ouvrir l'image avec Pillow
            img_origine = Image.open(image_path)

            # Conditionnellement convertir l'image en mode RGB
            if img_origine.mode != 'RGB':
                img_origine = img_origine.convert('RGB')

            # Convertir l'image en tableau NumPy
            r = np.array(img_origine)

            # Utiliser 'r' pour la prédiction avec le modèle YOLO
            model = YOLO("runs/detect/train5/weights/best.pt")
            model.predict(r, save=True, save_crop=True, classes=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],project="static", exist_ok=True)
        return True

    except Exception as e:
        print(f"Erreur lors de la prédiction : {e}")
        return False



# predir("imageTest/CV_Emine_Youbah.pdf")





# ================================================================================
def clean_and_format_text(text):
    # Supprimer les caractères non imprimables
    cleaned_text = ''.join(char for char in text if char.isprintable())

    # Remplacer les séquences de saut de ligne par des espaces
    cleaned_text = cleaned_text.replace('\n', ' ')

    # Supprimer les espaces multiples
    cleaned_text = ' '.join(cleaned_text.split())

    return cleaned_text



def extract_text_from_images(image_paths):
    try:
        extracted_texts = []

        for image_path in image_paths:
            # Ouvrir l'image à l'aide de PIL (Pillow)
            image = Image.open(image_path)

            # Utiliser pytesseract pour extraire le texte
            extracted_text = pytesseract.image_to_string(image)

            # Ajouter le texte extrait à la liste
            extracted_texts.append(extracted_text)

        return extracted_texts
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return None

# =========================================================
# Exemple d'utilisation
# image_paths_list = ['runs/detect/predict4/crops/Profil/image0.jpg', 'runs/detect/predict4/crops/Profil/image02.jpg']
# result_texts_list = extract_text_from_images(image_paths_list)
# print(result_texts_list)

# Appliquer la fonction de nettoyage et de formatage à chaque texte
# cleaned_and_formatted_texts = [clean_and_format_text(text) for text in result_texts_list]
#
# # Afficher les résultats optimisés
# for i, text in enumerate(cleaned_and_formatted_texts, start=1):
#     print(f'Texte {i}: {text}\n')
# ===========================================================



def build_image_dictionary(parent_folder):
    # Initialiser le dictionnaire
    image_dict = {}

    # Liste des fichiers dans le dossier parent
    files = os.listdir(parent_folder)

    # Parcourir chaque fichier
    for file in files:
        file_path = os.path.join(parent_folder, file)

        # Vérifier si c'est un dossier
        if os.path.isdir(file_path):
            # Liste des static dans le dossier
            # static = [os.path.join(file_path, image) for image in os.listdir(file_path) if image.lower().endswith(('.png', '.jpg', '.jpeg'))]
            images = [os.path.join(file_path, image) for image in os.listdir(file_path)]
            # Si le dossier a des static, ajouter au dictionnaire
            if images:
                # Utiliser le nom du dossier comme clé
                # if file != "Picture":
                image_dict[file] = images

    return image_dict


# ========================================================================================
# Exemple d'utilisation
parent_folder_path = 'static/predict/crops'
# result_dict = build_image_dictionary(parent_folder_path)
#
# # Afficher le dictionnaire résultant
# for key, value in result_dict.items():
#     print(f"{key}: {value}")
# =========================================================================================

# Afficher le dictionnaire résultant
def infocv():
    dict = {}
    for key, value in build_image_dictionary(parent_folder_path).items():
        result_texts_list = extract_text_from_images(value)
        cleaned_and_formatted_texts = [clean_and_format_text(text) for text in result_texts_list]
        textfi = str(cleaned_and_formatted_texts)
        dict[key] = textfi

    return dict


# # Afficher les résultats optimisés
# for key, text in infocv().items():
#     print(f'"{key}": {text}\n')


