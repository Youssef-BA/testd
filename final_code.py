import extract_msg as msg
from PIL import Image, ImageSequence
import easyocr
import imghdr
import io
import numpy as np
import re
from texttable import Texttable  # Importer Texttable pour afficher les tableaux

def extract_msg_with_tif(file_path):
    # Charger le fichier .msg
    message = msg.Message(file_path)

    # Extraire les informations principales
    subject = message.subject
    sender = message.sender
    to = message.to
    date = message.date
    body = message.body

    # Afficher les informations du fichier .msg
    print(f"Subject: {subject}")
    print(f"From: {sender}")
    print(f"To: {to}")
    print(f"Date: {date}")
    print("\nBody:")
    print(body)

    # Initialiser une structure pour stocker les résultats
    all_extracted_data = []

    # Vérifier et traiter les pièces jointes
    if message.attachments:
        for attachment in message.attachments:
            print(f"\nProcessing attachment: {attachment.longFilename}")
            
            # Vérifier le type de fichier
            file_type = imghdr.what(None, h=attachment.data)
            if file_type != 'tiff':
                print(f"Attachment {attachment.longFilename} is not a valid TIFF file (detected type: {file_type}). Skipping.")
                continue

            # Charger le fichier TIFF avec PIL via BytesIO
            try:
                with io.BytesIO(attachment.data) as tif_stream:
                    with Image.open(tif_stream) as img:
                        reader = easyocr.Reader(['en', 'fr'])  # Initialiser le lecteur OCR

                        # Traiter chaque page du fichier TIFF
                        full_text = ""
                        for page_number, page in enumerate(ImageSequence.Iterator(img), start=1):
                            # Convertir la page en format compatible
                            page = page.convert("RGB")
                            page_np = np.array(page)
                            
                            # Extraire le texte
                            text = reader.readtext(page_np, detail=0)
                            page_text = "\n".join(text)
                            full_text += f"--- Texte de la page {page_number} ---\n{page_text}\n"
                        
                        # Appliquer regex pour extraire les données importantes
                        extracted_data = extract_important_information(full_text)
                        all_extracted_data.append(extracted_data)

                        # Afficher les données extraites
                        print(f"--- Données extraites de {attachment.longFilename} ---")
                        print(extracted_data)

            except Exception as e:
                print(f"Error processing TIFF file {attachment.longFilename}: {e}")
    else:
        print("No attachments found in the .msg file.")

    return all_extracted_data

def extract_important_information(text):
    # Liste des regex pour chaque information
    regex_patterns = {
        "emetteur_nom": r"From:\s*(.+)",  # Nom de l'émetteur
        "recepteur_nom": r"To:\s*(.+)",  # Nom du récepteur
        "iban": r"IBAN\s+IBAN\s+(FR\d{2}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{3})",
        "swift": r"Swift:\s+([A-Z0-9]{8,11})",
        "montant": r"Veuillez virer la somme de\s+Please\s+([\d,]+\.\d{2}) EUR",
        "date_compensation": r"Date de valeur compensée\s+(\d{2}/\d{2}/\d{4})",
        "nom_beneficiaire": r"Nom bénéficiaire\s+Beneficiary name\s+(.+)",
        "banque_beneficiaire": r"Banque bénéficiaire\s+Beneficiary bank\s+(.+)",
        "transfer_id": r"Transfer id\s*(\d+)"
    }

    # Appliquer les regex sur le texte
    data = {key: re.findall(pattern, text) for key, pattern in regex_patterns.items()}

    # Organisation des données extraites
    extracted_data = {
        "Émetteur": data["emetteur_nom"][0] if data["emetteur_nom"] else None,
        "Récepteur": data["recepteur_nom"][0] if data["recepteur_nom"] else None,
        "IBAN": data["iban"],
        "Swift": data["swift"],
        "Montant à virer": data["montant"],
        "Date de compensation": data["date_compensation"],
        "Nom du bénéficiaire": data["nom_beneficiaire"],
        "Banque bénéficiaire": data["banque_beneficiaire"],
        "Transfer ID": data["transfer_id"]
    }

    return extracted_data

# Chemin vers le fichier .msg
file_path = "test.msg"
output = extract_msg_with_tif(file_path)

def display_data_with_texttable(data_list):
    table = Texttable()
    # Ajouter l'en-tête
    headers = ["ID_MAIL", "Émetteur", "Récepteur", "IBAN", "Swift", "Montant à virer", "Date de compensation", "Nom du bénéficiaire", "Banque bénéficiaire", "Transfer ID"]
    table.header(headers)

    # ID unique pour chaque mail
    id_mail = 1

    # Ajouter les lignes
    for row in data_list:
        # Extraire les listes ou valeurs simples
        ibans = row.get("IBAN", [])
        swifts = row.get("Swift", [])
        montants = row.get("Montant à virer", [])
        dates = row.get("Date de compensation", [])
        beneficiaires = row.get("Nom du bénéficiaire", [])
        banques = row.get("Banque bénéficiaire", [])
        transfer_id = row.get("Transfer ID", [])

        # Trouver le nombre maximum de lignes nécessaires
        max_rows = max(len(ibans), len(swifts), len(montants), len(dates), len(beneficiaires), len(banques), 1)

        # Ajouter une ligne pour chaque élément
        for i in range(max_rows):
            table.add_row([
                id_mail,  # ID unique pour chaque mail
                row.get("Émetteur", ""),  # Émetteur affiché uniquement pour la première ligne
                row.get("Récepteur", ""),  # Récepteur affiché uniquement pour la première ligne
                ibans[i] if i < len(ibans) else "",  # IBAN
                swifts[i] if i < len(swifts) else "",  # Swift
                montants[i] if i < len(montants) else "",  # Montant
                dates[i] if i < len(dates) else "",  # Date
                beneficiaires[i] if i < len(beneficiaires) else "",  # Nom du bénéficiaire
                banques[i] if i < len(banques) else "",  # Banque bénéficiaire
                transfer_id[i] if len(transfer_id) else ""
            ])
        
        id_mail += 1  # Incrémenter l'ID pour le mail suivant

    # Afficher le tableau
    print(table.draw())


# Appeler la fonction pour afficher le tableau
print("\n--- Tableau affiché avec Texttable ---")
display_data_with_texttable(output)
