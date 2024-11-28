import extract_msg as msg
import re

def extract_success_blocks(body):
    """
    Extrait les blocs contenant 'Results: Success' ligne par ligne.
    """
    lines = body.splitlines()
    blocks = []
    current_block = []
    success_blocks = []
    
    # Parcourir les lignes une par une
    for line in lines:
        if line.startswith("Date:"):  # Un nouveau bloc commence
            if current_block:  # Si un bloc est déjà en cours, on le traite
                blocks.append("\n".join(current_block))
            current_block = [line]  # Commence un nouveau bloc
        elif line.strip() == "":  # Ligne vide, ignorer
            continue
        else:
            current_block.append(line)  # Ajouter la ligne au bloc en cours

    # Ajouter le dernier bloc s'il existe
    if current_block:
        blocks.append("\n".join(current_block))

    # Filtrer les blocs contenant "Results: Success"
    for block in blocks:
        if "Results: Success" in block:
            success_blocks.append(block)

    return success_blocks


def process_msg_file(file_path):
    """
    Charge un fichier .msg et extrait les blocs pertinents contenant 'Results: Success'.
    """
    # Charger le fichier .msg
    msg_file = msg.Message(file_path)

    # Extraire le corps du message
    body_text = msg_file.body

    # Extraire les blocs avec "Results: Success"
    success_blocks = extract_success_blocks(body_text)

    # Vérifier si des blocs sont trouvés
    if not success_blocks:
        print(f"Le fichier {file_path} ne contient aucun bloc avec 'Results: Success'.")
        return None

    # Retourner les blocs trouvés
    return success_blocks


# Chemin vers le fichier .msg
file_path = "test.msg"

# Traiter le fichier et afficher les résultats
results = process_msg_file(file_path)

if results:
    print("Blocs extraits contenant 'Results: Success' :")
    for i, block in enumerate(results, start=1):
        print(f"{block}")
