import extract_msg

def process_msg_file(file_path):
    """
    Traite un fichier .msg pour extraire son corps.
    """
    msg_file = extract_msg.Message(file_path)
    body_text = msg_file.body
    return body_text

