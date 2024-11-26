import extract_msg as msg
import re

def extract_important_information_from_body(body):
    # Filtrer les sections contenant "Results: Success"
    success_blocks = re.findall(
        r"(Date:\s*\d{2}/\d{2}/\d{4}.*?Results:\s*Success.*?Elapsed time:\s*\d{2}:\d{2}:\d{2})",
        body,
        re.DOTALL
    )

    # Si aucune section avec "Results: Success" n'est trouvée, retourner une liste vide
    if not success_blocks:
        return []

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


# Charger le fichier .msg et extraire les informations
file_path = "test.msg"

# Charger le message avec extract_msg
msg_file = msg.Message(file_path)

# Extraire le corps du message
body_text = msg_file.body

# Appeler la fonction pour extraire les informations pertinentes
results = extract_important_information_from_body(body_text)

# Afficher les résultats
for result in results:
    print(result)
