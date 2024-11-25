from PIL import Image, ImageSequence
import easyocr
import numpy as np

# Chemin vers le fichier TIFF
file_path = "fax.tif"

# Initialiser le lecteur EasyOCR
reader = easyocr.Reader(['en', 'fr'])  # Ajoutez les langues nécessaires

# Ouvrir le fichier TIFF et itérer sur les pages
with Image.open(file_path) as img:
    for page_number, page in enumerate(ImageSequence.Iterator(img), start=1):
        # Convertir la page en format compatible avec OpenCV
        page = page.convert("RGB")  # EasyOCR nécessite un format RGB
        page_np = np.array(page)
        
        # Extraire le texte de la page
        text = reader.readtext(page_np, detail=0)
        
        # Afficher le texte extrait pour la page
        print(f"--- Texte de la page {page_number} ---")
        print("\n".join(text))
        print("\n")