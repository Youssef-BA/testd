import extract_msg as msg
from PIL import Image, ImageSequence
import easyocr
import imghdr
import io
import numpy as np

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
                        for page_number, page in enumerate(ImageSequence.Iterator(img), start=1):
                            # Convertir la page en format compatible
                            page = page.convert("RGB")
                            page_np = np.array(page)
                            
                            # Extraire le texte
                            text = reader.readtext(page_np, detail=0)
                            
                            # Afficher le texte extrait
                            print(f"--- Texte de la page {page_number} ---")
                            print("\n".join(text))
                            print("\n")
            except Exception as e:
                print(f"Error processing TIFF file {attachment.longFilename}: {e}")
    else:
        print("No attachments found in the .msg file.")

# Chemin vers le fichier .msg
file_path = "test.msg"
extract_msg_with_tif(file_path)
