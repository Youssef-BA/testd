import re

def extract_address(page_content):
    """
    Extrait l'adresse complète du destinataire, y compris le code postal et la ville.
    """
    lines = page_content.splitlines()
    address_lines = []
    capture = False

    for i, line in enumerate(lines):
        # Début de l'adresse
        if re.match(r"^\d+,\s*", line):
            capture = True
            address_lines.append(line.strip())
            continue

        # Pendant la capture, ajouter les lignes pertinentes
        if capture:
            if re.match(r"^\d{5}\s+[A-Za-zÀ-ÿ\s]+$", line):  # Code postal et ville
                address_lines.append(line.strip())
                break  # Adresse complète, arrêt
            elif re.match(r"^[A-Za-zÀ-ÿ\s]+$", line):  # Rue ou autre
                address_lines.append(line.strip())

    # Retourner l'adresse complète formatée
    return " ".join(address_lines)

def extract_important_information_by_page(text):
    """
    Extrait les informations nécessaires pour chaque page distinctement,
    applique les transformations demandées et inclut les corrections spécifiques.
    """
    # Définition des motifs regex pour les informations globales
    global_patterns = {
        "OBJET": r"NOTES:\s*(.+)",
        "fax_destinataire": r"Fax:\s*(\d+)",
        "Expéditeur": r"E-mail:\s*([\w\.-]+(?:\s*\.\s*[\w\.-]*)*\s*@\s*[\w\.-]+)",
        "Titre de l'expéditeur": r"From:\s*(.+)"
    }
    # Définition des motifs regex pour les informations spécifiques aux pages
    page_patterns = {
        "Entité": r"4\s*44\s*=\s*([A-Z\s]+)\n[A-Z\s]+\n",
        "Direction": r"Direction[^\n]*\n(?:[^\n]*\n?){0,1}",
        "contact1AXA": r"([A-Za-zÀ-ÿ]+(?: [A-Za-zÀ-ÿ]+)*)\s*((?:\d{2}\s*){4,5})",
        "Destinataire": r"4\s*44\s*=\s*(?:[A-Z\s]+\n)*([A-Z\s]+)\n",
        "Tel Destinataire": r"Tel\s*\n([\d\s]+)",
        "Fax Destinataire": r"Fax\s*\n([\d\s]+)",
        "Mails": r"Mail\s*([\w\.-]+(?:\s[\w\.-]*)*@[\w\.-]+)",
        "Date Document": r"(Paris\s*,\s*le\s*/\s*on\s*\d{2}/\d{2}/\d{4})",
        "Référence": r"Our\s+reference\s+(\d+)",
        "Compte à débiter": r"From\s*\n([A-Z0-9\s]+)",
        "SWIFT": r"Swift:\s*([A-Z0-9]+)",
        "Titulaire de compte": r"Swift:\s*[A-Z0-9]+\s*(.*\n.*)",
        "Montant décaissement": r"Veuillez virer la somme de\s*Please\s*([\d,]+\.\d{2})\s([A-Z]{3})",
        "Date valeur compensée": r"Date de valeur compensée\s*(\d{2}/\d{2}/\d{4})",
        "Bénéficiaire": r"Nom bénéficiaire\s*Beneficiary name\s*([A-ZÀ-ÿ\s\n]+?)\s*IBAN",
        "IBAN Bénéficiaire": r"IBAN\s*IBAN\s*([A-Z0-9\s]+)\s*Banque bénéficiaire",
        "Banque Bénéficiaire": r"Banque bénéficiaire\s*Beneficiary bank\s*([A-Z]+)",
        "Swift Bénéficiaire": r"Code Swift\s*Swift code\s*([A-Z0-9]+)",
        "Commission": r"Swift code\s*[A-Z0-9]+\s*([^\n]+)",
        "Motif du paiement": r"Motif du paiement\s*Payment purpose\s*([^\n]+)",
        "Référence de l'opération": r"(id \d+)",
        "Signataire1": r"Signatures autorisées\s*Authorized signatures\s*([A-Za-zÀ-ÿ\s]+)",
        "Signataire2": r"Signatures autorisées\s*Authorized signatures\s*([A-Za-zÀ-ÿ\s]+)"
    }

    # Diviser le texte en pages
    pages = text.split("--- Page ")

     # Recherche des informations globales dans toutes les pages
    # Extraction des informations globales à partir de la page 2
    global_data = {}
    if len(pages) > 1:
        for key, pattern in global_patterns.items():
            match = re.findall(pattern, pages[1])  # Page 2
            if match:
                global_data[key] = match[0].strip()
    
    # Appliquer une transformation spécifique à l'Expéditeur
    if "Expéditeur" in global_data and global_data["Expéditeur"]:
        global_data["Expéditeur"] = global_data["Expéditeur"].replace(" ", "")

    # Extraction des informations spécifiques pour chaque page
    extracted_data = {}
    for page_number, page_content in enumerate(pages, start=1):
        if not page_content.strip():
            continue

        page_data = {}

        # Extraire chaque champ défini dans les regex
        for key, pattern in page_patterns.items():
            match = re.findall(pattern, page_content)
            page_data[key] = match[0] if match else None
            if key == "contact1AXA":  # Séparer les contacts
                page_data["Contact AXA 1"] = (
                    " ".join(match[0]).replace("\n", "") if len(match) > 0 else None
                )
                page_data["Contact AXA 2"] = (
                    " ".join(match[1]).replace("\n", "") if len(match) > 1 else None
                )
                page_data["Contact AXA 3"] = (
                    " ".join(match[2]).replace("\n", "") if len(match) > 2 else None
                )
            elif key == "Montant décaissement":  # Diviser le montant et la devise
                if match:
                    page_data["Montant décaissement"] = match[0][0]
                    page_data["Devise"] = match[0][1]
                else:
                    page_data["Montant décaissement"] = None
                    page_data["Devise"] = None
            elif key == "Référence de l'opération":  # Capture élargie pour les références
                page_data["Référence de l'opération"] = match[0] if match else None
        # Ajout de l'adresse
        page_data["Adresse Destinataire"] = extract_address(page_content)

        # Sélectionner le bon Mail Destinataire
        mails = re.findall(page_patterns["Mails"], page_content)
        if len(mails) > 1:
            page_data["Mail Destinataire"] = mails[1]
        elif mails:
            page_data["Mail Destinataire"] = mails[0]
        else:
            page_data["Mail Destinataire"] = None

        if "Entité" in page_data and page_data["Entité"]:
            page_data["Entité"] = page_data["Entité"].replace("\n", " ")
        if "Direction" in page_data and page_data["Direction"]:
            page_data["Direction"] = page_data["Direction"].replace("\n", " ")
        # Nettoyage des champs
        if "Tel Destinataire" in page_data and page_data["Tel Destinataire"]:
            page_data["Tel Destinataire"] = page_data["Tel Destinataire"].replace("\n", "")

        if "Fax Destinataire" in page_data and page_data["Fax Destinataire"]:
            page_data["Fax Destinataire"] = page_data["Fax Destinataire"].replace("\n", "")

        if "Mail Destinataire" in page_data and page_data["Mail Destinataire"]:
            page_data["Mail Destinataire"] = page_data["Mail Destinataire"].replace(" ", ".")

        if "Compte à débiter" in page_data and page_data["Compte à débiter"]:
            page_data["Compte à débiter"] = page_data["Compte à débiter"].replace("\n", "")

        if "Titulaire de compte" in page_data and page_data["Titulaire de compte"]:
            page_data["Titulaire de compte"] = page_data["Titulaire de compte"].replace("\n", " ")

        if "Bénéficiaire" in page_data and page_data["Bénéficiaire"]:
            page_data["Bénéficiaire"] = page_data["Bénéficiaire"].replace("\n", " ")

        if "IBAN Bénéficiaire" in page_data and page_data["IBAN Bénéficiaire"]:
            page_data["IBAN Bénéficiaire"] = page_data["IBAN Bénéficiaire"].replace("\n", "")

        if "Motif du paiement" in page_data and page_data["Motif du paiement"]:
            page_data["Motif du paiement"] = page_data["Motif du paiement"].replace("|", "/")

        if "Signataire1" in page_data and page_data["Signataire1"]:
            page_data["Signataire1"] = page_data["Signataire1"].split("\n")[0]

        if "Signataire2" in page_data and page_data["Signataire2"]:
            page_data["Signataire2"] = page_data["Signataire2"].split("\n")[1]

        extracted_data[f"Page {page_number}"] = page_data

        # Propager les informations globales à toutes les pages
    for page_number, page_data in extracted_data.items():
        page_data.update(global_data)

    # Supprimer la première page après extraction des données globales
    if "Page 2" in extracted_data:
        extracted_data.pop("Page 2")
    return extracted_data
