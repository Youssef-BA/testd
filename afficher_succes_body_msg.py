import extract_msg as msg
import re

def extract_important_information_from_body(body):
    """
    Extrait les blocs d'information pertinents dans le corps d'un email, mais seulement
    si le corps contient au moins un "Results: Success".
    """
    # Vérifier si "Results: Success" est présent dans le corps
    if "Results: Success" not in body:
        return None  # Ignorer ce corps s'il ne contient pas "Results: Success"

    # Filtrer les sections contenant "Results: Success"
    success_blocks = re.findall(
        r"(Date:\s*\d{2}/\d{2}/\d{4}.*?Results:\s*Success.*?Elapsed time:\s*\d{2}:\d{2}:\d{2})",
        body,
        re.DOTALL
    )

    if not success_blocks:
        return None  # Si aucun bloc filtré n'est trouvé, ignorer ce corps

    # Liste des regex pour extraire les informations spécifiques
    regex_patterns = {
        "date": r"Date:\s*(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})",  # Date complète
        "sent_for": r"Sent for\s*(\d+)",  # Numéro envoyé pour
        "remote_id": r"remote ID\s*([A-Za-z0-9]+)",  # Remote ID
        "results": r"Results:\s*(Success)",  # Résultat (Success)
        "nb_pages": r"Nb of pages:\s*(\d+)",  # Nombre de pages
        "elapsed_time": r"Elapsed time:\s*(\d{2}:\d{2}:\d{2})",  # Temps écoulé
    }

    extracted_data = []

    # Parcourir chaque bloc filtré
    for block in success_blocks:
        # Appliquer les regex pour extraire les données de chaque bloc
        data = {key: re.search(pattern, block) for key, pattern in regex_patterns.items()}
        # Nettoyer les résultats (extraction des groupes correspondants)
        clean_data = {key: match.group(1) if match else None for key, match in data.items()}
        extracted_data.append(clean_data)

    return extracted_data


def process_msg_file(file_path):
    """
    Charge un fichier .msg, vérifie si le corps contient "Results: Success",
    et extrait les informations pertinentes si présent.
    """
    # Charger le fichier .msg
    msg_file = msg.Message(file_path)

    # Extraire le corps du message
    body_text = msg_file.body

    # Vérifier et extraire les informations seulement si "Results: Success" est présent
    important_info = extract_important_information_from_body(body_text)

    # Si rien n'est extrait, retourner un message d'avertissement
    if not important_info:
        print(f"Le fichier {file_path} ne contient aucun 'Results: Success'.")
        return None

    # Sinon, retourner les informations extraites
    return important_info


# Chemin vers le fichier .msg
file_path = "test.msg"

# Traiter le fichier et afficher les résultats si pertinents
results = process_msg_file(file_path)

if results:
    print("Informations extraites :")
    for result in results:
        print(result)
