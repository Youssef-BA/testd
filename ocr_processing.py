import io
from PIL import Image, ImageSequence
import numpy as np
import easyocr
from regex_extraction import extract_important_information_by_page
import extract_msg


message = extract_msg.Message("test.msg")
def process_tif_attachments(message):
    """
    Traite les pièces jointes au format .tif d'un fichier .msg pour extraire les données.
    """
    all_extracted_data = []
    reader = easyocr.Reader(['en', 'fr'])

    if message.attachments:
        for attachment in message.attachments:
            try:
                with io.BytesIO(attachment.data) as tif_stream:
                    with Image.open(tif_stream) as img:
                        full_text = ""
                        for page_number, page in enumerate(ImageSequence.Iterator(img), start=1):
                            page = page.convert("RGB")
                            page_np = np.array(page)
                            text = reader.readtext(page_np, detail=0)
                            full_text += f"--- Page {page_number} ---\n" + "\n".join(text) + "\n"

                        extracted_data = extract_important_information_by_page(full_text)
                        all_extracted_data.append(extracted_data)

            except Exception as e:
                print(f"Error processing TIFF file {attachment.longFilename}: {e}")

    return all_extracted_data
