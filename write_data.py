import pandas as pd

def write_data_to_txt(data_list, success_data, output_filename="output.txt"):
    """
    Write the extracted data to a .txt file using | as a delimiter.
    Includes information like DATE HEURE ACCUSE DE RECEPTION, DATE HEURE ENVOI, N page, Duree envoi.
    """
    # Define the column order as per the new requirements
    column_order = [
        "OBJET", "fax_destinataire", "Expéditeur", "DATE HEURE ACCUSE DE RECEPTION", "DATE HEURE ENVOI", "N page", "Duree envoi", "Titre de l'expéditeur",
        "Entité", "Direction", "Contact AXA 1", "Contact AXA 2", "Contact AXA 3",
        "Destinataire", "Adresse Destinataire", "Tel Destinataire",
        "Fax Destinataire", "Mail Destinataire", "Date document",
        "Référence", "Compte à débiter", "SWIFT", "Titulaire de compte",
        "Montant décaissement", "Devise", "Date valeur compensée", "Bénéficiaire",
        "IBAN Bénéficiaire", "Banque Bénéficiaire", "Swift Bénéficiaire",
        "Commission", "Motif du paiement", "Référence de l'opération",
        "Signataire1", "Signataire2"
        
    ]

    # Open the file for writing
    with open(output_filename, 'w', encoding='utf-8') as f:
        # Write the header row
        f.write("|".join(column_order) + "\n")

        # Write the data rows
        for i, page_data in enumerate(data_list):
            for page_name, row in page_data.items():
                # Merge success_data (from extract_success_blocks) into each page's row
                success_info = success_data[i] if i < len(success_data) and isinstance(success_data[i], dict) else {}

                if not isinstance(row, dict):
                    raise ValueError(f"Invalid row format: Expected dictionary, got {type(row)}")

                # Update row with success_info
                row.update(success_info)

                # Prepare a single row of data
                line = [
                    str(row.get(col, "")) for col in column_order
                ]
                # Write the row to the file, separated by |
                f.write("|".join(line) + "\n")

    print(f"Data successfully written to {output_filename}")
