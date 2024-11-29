"""
-------- Extrait les blocs contenant 'Results: Success' ligne par ligne -------------- 
Cette Partie est responsable de l'extraction des blocs contenant 'Results: Success'.
"""

def extract_success_blocks(body):
    lines = body.splitlines()
    blocks = []
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

    return [block for block in blocks if "Results: Success" in block]
