from process_msg import process_msg_file
from extract_success import extract_success_blocks
from ocr_processing import process_tif_attachments
from regex_extraction import extract_important_information
import extract_msg
from write_data import write_data_to_txt

def main():
    """
    Programme principal qui effectue les étapes suivantes :
    1. Extraire le texte principal d'un fichier .msg
    2. Extraire les blocs "Results: Success" du texte principal
    3. Traiter les fichiers TIFF attachés au fichier .msg
    4. Sauvegarder fichier format .txt
    """
    
    file_path = "test.msg"
    output_filename="output.txt"
    # Étape 1 : Extraire le texte principal
    print("\n--- Traitement du fichier .msg ---")
    body_text = process_msg_file(file_path)

    # Étape 2 : Extraire les blocs "Results: Success"
    print("\n--- Extraction des blocs 'Results: Success' ---")
    success_blocks = extract_success_blocks(body_text)
    for block in success_blocks:
        print(block)

    # Étape 3 : Traiter les fichiers TIFF attachés
    print("\n--- Traitement des pièces jointes TIFF ---")
    message = extract_msg.Message(file_path)
    extracted_data = process_tif_attachments(message)

    # Étape 4 : Afficher les données
    print("\n--- Sauvegarder sous format .txt ---")
    # Écrire les données extraites dans un fichier texte
    write_data_to_txt(extracted_data, output_filename)


if __name__ == "__main__":
    main()
