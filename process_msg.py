import extract_msg

def process_msg_file(file_path):
    """
    Traite un fichier .msg pour extraire son corps.
    """
    msg_file = extract_msg.Message(file_path)
    body_text = msg_file.body
    return body_text

import extract_msg

def extract_send_date(file_path):
    """
    Extrait la date et l'heure d'envoi d'un email à partir d'un fichier .msg.
    """
    try:
        msg = extract_msg.Message(file_path)
        send_date = msg.date  # Renvoie un objet datetime
        if send_date:
            return send_date.strftime("%d/%m/%Y %H:%M:%S")  # Formatage en chaîne
        else:
            return None
    except Exception as e:
        print(f"Erreur lors de l'extraction de la date d'envoi : {e}")
        return None