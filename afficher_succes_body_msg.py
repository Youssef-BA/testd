import extract_msg as msg
import re

def extract_success_blocks(body):
    """
    Extrait uniquement les blocs contenant 'Results: Success' depuis le corps d'un email.
    """
    # Expression régulière pour extraire les blocs spécifiques contenant "Results: Success"
    success_blocks = re.findall(
        r"(Date:\s*\d{2}/\d{2}/\d{4}.*?Results:\s*Success.*?Elapsed time:\s*\d{2}:\d{2}:\d{2})",
        body,
        re.DOTALL
    )

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
