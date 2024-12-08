from qr_lib.QrToFile import QrsToFile
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import sys
from PIL import Image
import os 


path = r"C:\dev\QrTransfer\qr_data_QrTransfer_2024-12-08_15-41-38"
qrtofilehandler = QrsToFile()

def decoder(image):
    barcode = decode(image)
    for obj in barcode:
        barcodeData = obj.data
        print(barcodeData)
        if(qrtofilehandler.parseFilePart(barcodeData)):
                with open(qrtofilehandler.file_name + "RECIEVED","wb") as file:
                    file.write(qrtofilehandler.full_file_data)
                sys.exit()
        
files = os.listdir(path)
for file in files:
    with Image.open(path + '\\' + file) as image_current:
        decoder(image_current)






