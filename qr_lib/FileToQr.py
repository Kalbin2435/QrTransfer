import base64
from multiprocessing import Pool,Manager
import os
from datetime import datetime
import qrcode
from PIL import Image
import cv2
import numpy as np
import time
from io import BytesIO

def translateFileToQrs(path):
    # Generate data directory name but do not actually create it or chdir into it
    # (If you only want to display, you may skip directory creation altogether)
    dirname = _make_data_directory_name(path)

    with open(path, "rb") as file:
        data = file.read()
        ascii_bytes = base64.b64encode(data)

    # Instead of creating images on disk, store them in a list
    images = _createImagesFromData(ascii_bytes)

    number = _number_to_padded_byte_number(0)
    filename = bytes(os.path.basename(path), "ascii")
    file_counter = len(images) + 1 # since we will add one more QR for metadata
    file_count = _number_to_padded_byte_number(file_counter)
    first_qr_data = number + file_count + filename

    # Create the first (metadata) QR image and prepend it to the list
    metadata_image = _qrcodeMakeImage(first_qr_data)
    images.insert(0, metadata_image)

    # Now display all the images as a slideshow
    display_images_as_slideshow(images, delay=0.5)

def _qrcodeMakeImage(data):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(data, optimize=0)
    qr.make(fit=True)
    img = qr.make_image()  # This is a PIL Image
    return img

def _number_to_padded_byte_number(number, digits=4):
    number = f'{number:0{digits}}'
    number = bytes(number, "ascii")
    return number


def _createImageBytesFromData(chunk_data):
    img = _qrcodeMakeImage(chunk_data)
    byte_io = BytesIO()
    img.save(byte_io) 
    return byte_io.getvalue() 

def _createImagesFromData(data, bytes_per_image=2900):
    index = 1
    chunks = []
    while len(data) > 0:
        chunk = data[:bytes_per_image]
        data = data[bytes_per_image:]
        chunk_data = _number_to_padded_byte_number(index) + chunk
        chunks.append(chunk_data)
        index += 1
    
    print("Chunks to make:" + str(len(chunks)))

    with Pool() as pool:
        images_data = pool.map(_createImageBytesFromData, chunks)

    images = [Image.open(BytesIO(img_data)) for img_data in images_data]
    return images

def _make_data_directory_name(path):
    filename_no_ext = os.path.splitext(os.path.basename(path))[0]
    return "qr_data_" + filename_no_ext + "_" + _get_file_writable_date()

def _get_file_writable_date():
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y-%m-%d_%H-%M-%S")
    return formatted_date

def display_images_as_slideshow(images, delay=0.5, width=600, height=600):
    # Create a named window that can be resized
    cv2.namedWindow('QR Slideshow', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('QR Slideshow', width, height)

    while True:
        for img in images:
            # Ensure the image is RGB
            img = img.convert("RGB")

            # Convert PIL image to OpenCV format
            opencv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

            # Optionally resize the image to fit the desired window size
            opencv_img = cv2.resize(opencv_img, (width, height))

            cv2.imshow('QR Slideshow', opencv_img)
            key = cv2.waitKey(int(delay * 300))
            if key == ord('q'):
                break
    cv2.destroyAllWindows()
