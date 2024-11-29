import pandas as pd

def write_data_to_txt(data_list, output_filename="output.txt"):
    with open(output_filename, 'w', encoding='utf-8') as f:
        # Ajouter l'en-tête
        headers = [
            "OBJET", 
            "fax_destinataire", 
            "Expéditeur", 
            "Titre de l'expéditeur", 
            "Entité", 
            "Direction", 
            "Contact AXA", 
            "Destinataire", 
            "Tel Destinataire", 
            "Fax Destinataire", 
            "Mail Destinataire", 
            "Date Document", 
            "Référence", 
            "Compte à débiter", 
            "SWIFT", 
            "Titulaire de compte", 
            "Montant décaissement", 
            "Devise", 
            "Date valeur compensée", 
            "Bénéficiaire", 
            "IBAN Bénéficiaire", 
            "Banque Bénéficiaire", 
            "Swift Bénéficiaire", 
            "Commission", 
            "Motif du paiement", 
            "Référence de l'opération", 
            "Signataire1", 
            "Signataire2"
        ]
        # Écrire les en-têtes dans le fichier
        f.write("|".join(headers) + "\n")

        # Ajouter les lignes de données
        for row in data_list:
            # Trouver le nombre maximum de lignes nécessaires
            max_rows = max(len(row.get(key, [])) for key in headers)
            # Ajouter une ligne pour chaque élément
            for i in range(max_rows):
                # Récupérer chaque valeur et gérer les indices
                line = [
                    row.get("OBJET", ""),
                    row.get("fax_destinataire", ""),
                    row.get("Expéditeur", ""),
                    row.get("Titre de l'expéditeur", ""),
                    row.get("Entité", [""])[i] if i < len(row.get("Entité", [])) else "",
                    row.get("Direction", [""])[i] if i < len(row.get("Direction", [])) else "",
                    row.get("Contact AXA", [""])[i] if i < len(row.get("Contact AXA", [])) else "",
                    row.get("Destinataire", [""])[i] if i < len(row.get("Destinataire", [])) else "",
                    row.get("Tel Destinataire", [""])[i] if i < len(row.get("Tel Destinataire", [])) else "",
                    row.get("Fax Destinataire", [""])[i] if i < len(row.get("Fax Destinataire", [])) else "",
                    row.get("Mail Destinataire", [""])[i] if i < len(row.get("Mail Destinataire", [])) else "",
                    row.get("Date Document", [""])[i] if i < len(row.get("Date Document", [])) else "",
                    row.get("Référence", [""])[i] if i < len(row.get("Référence", [])) else "",
                    row.get("Compte à débiter", [""])[i] if i < len(row.get("Compte à débiter", [])) else "",
                    row.get("SWIFT", [""])[i] if i < len(row.get("SWIFT", [])) else "",
                    row.get("Titulaire de compte", [""])[i] if i < len(row.get("Titulaire de compte", [])) else "",
                    row.get("Montant décaissement", [""])[i] if i < len(row.get("Montant décaissement", [])) else "",
                    row.get("Devise", [""])[i] if i < len(row.get("Devise", [])) else "",
                    row.get("Date valeur compensée", [""])[i] if i < len(row.get("Date valeur compensée", [])) else "",
                    row.get("Bénéficiaire", [""])[i] if i < len(row.get("Bénéficiaire", [])) else "",
                    row.get("IBAN Bénéficiaire", [""])[i] if i < len(row.get("IBAN Bénéficiaire", [])) else "",
                    row.get("Banque Bénéficiaire", [""])[i] if i < len(row.get("Banque Bénéficiaire", [])) else "",
                    row.get("Swift Bénéficiaire", [""])[i] if i < len(row.get("Swift Bénéficiaire", [])) else "",
                    row.get("Commission", [""])[i] if i < len(row.get("Commission", [])) else "",
                    row.get("Motif du paiement", [""])[i] if i < len(row.get("Motif du paiement", [])) else "",
                    row.get("Référence de l'opération", [""])[i] if i < len(row.get("Référence de l'opération", [])) else "",
                    row.get("Signataire1", [""])[i] if i < len(row.get("Signataire1", [])) else "",
                    row.get("Signataire2", [""])[i] if i < len(row.get("Signataire2", [])) else ""
                ]
                # Écrire la ligne dans le fichier séparée par le caractère "|"
                f.write("|".join(line) + "\n")
    print(f"Data written to {output_filename}")