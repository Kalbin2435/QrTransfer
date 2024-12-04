from typing import List
from pyzbar.pyzbar import decode
from PIL import Image, ImageFile

def decode_img(image: Image.Image) -> List[bytes]:
    decoded_data = decode(image)
    data = []
    for obj in decoded_data:
        data.append(obj.data)
    return data

