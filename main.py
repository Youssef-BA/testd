from process_msg import process_msg_file, extract_send_date
from extract_success import extract_success_blocks
from ocr_processing import process_tif_attachments
from regex_extraction import extract_important_information_by_page
import extract_msg
from write_data import write_data_to_txt

def main():
    """
    Programme principal pour traiter les emails et leurs pièces jointes.
    """

    file_path = "test.msg"

    # Étape 1 : Extraire le texte principal
    print("\n--- Traitement du fichier .msg ---")
    body_text = process_msg_file(file_path)

    # Étape 2 : Extraire la date et l'heure d'envoi
    print("\n--- Extraction de la DATE HEURE ACCUSE DE RECEPTION ---")
    send_date = extract_send_date(file_path)
    print(f"DATE HEURE ACCUSE DE RECEPTION : {send_date}")

    # Étape 3 : Extraire les blocs "Results: Success"
    print("\n--- Extraction des blocs 'Results: Success' ---")
    success_blocks = extract_success_blocks(body_text)
    for block in success_blocks:
        # Ajouter la DATE HEURE ACCUSE DE RECEPTION dans chaque bloc
        block["DATE HEURE ACCUSE DE RECEPTION"] = send_date
        print(block)

    # Étape 4 : Traiter les fichiers TIFF attachés
    print("\n--- Traitement des pièces jointes TIFF ---")
    message = extract_msg.Message(file_path)
    extracted_data = process_tif_attachments(message)

    # Étape 5 : Sauvegarder les données sous format .txt
    print("\n--- Sauvegarder sous format .txt ---")
    write_data_to_txt(extracted_data, success_blocks, output_filename="output.txt")

if __name__ == "__main__":
    main()


