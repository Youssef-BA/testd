"""
-------- Extrait les blocs contenant 'Results: Success' ligne par ligne -------------- 
Cette Partie est responsable de l'extraction des blocs contenant 'Results: Success'.
"""

import re

def extract_success_blocks(body):
    """
    Extract blocks containing 'Results: Success' and extract details like 
    DATE HEURE ACCUSE DE RECEPTION, N page, and Duree envoi.
    """
    lines = body.splitlines()
    blocks = []
    extracted_details = []

    current_block = []
    for line in lines:
        if line.startswith("Date:"):
            if current_block:
                blocks.append("\n".join(current_block))
            current_block = [line]
        elif line.strip():
            current_block.append(line)

    if current_block:
        blocks.append("\n".join(current_block))

    # Filter blocks that contain "Results: Success" and extract details
    for block in blocks:
        if "Results: Success" in block:
            # Extract details
            date_heure_accuse = re.search(r"Date:\s*([\d/]+\s[\d:]+)", block)
            n_page = re.search(r"Nb of pages:\s*(\d+)", block)
            duree_envoi = re.search(r"Elapsed time:\s*([\d:]+)", block)

            details = {
                "DATE HEURE ENVOI": date_heure_accuse.group(1) if date_heure_accuse else None,
                "N page": n_page.group(1) if n_page else None,
                "Duree envoi": duree_envoi.group(1) if duree_envoi else None,
            }

            # Append details and block
            extracted_details.append(details)
            print(f"\n--- Block Content ---\n{block}\n")
    
    return extracted_details
