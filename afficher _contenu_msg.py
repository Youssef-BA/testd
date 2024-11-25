import extract_msg as msg

def extract_msg_content(file_path):
    # Charger le fichier .msg
    message = msg.Message(file_path)

    # Extraire les informations principales
    subject = message.subject
    sender = message.sender
    to = message.to
    date = message.date
    body = message.body

    # Afficher les informations
    print(f"Subject: {subject}")
    print(f"From: {sender}")
    print(f"To: {to}")
    print(f"Date: {date}")
    print("\nBody:")
    print(body)

    # Gérer les pièces jointes
    if message.attachments:
        print("\nAttachments:")
        for attachment in message.attachments:
            print(f"- {attachment.longFilename}")
            # Vous pouvez sauvegarder l'attachement si nécessaire :
            # with open(attachment.longFilename, 'wb') as f:
            #     f.write(attachment.data)

# Chemin vers le fichier .msg
file_path = "test.msg"
extract_msg_content(file_path)
