import cv2
import numpy as np
from pyzbar.pyzbar import decode
import base64
import ctypes
import sys


def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)

    for obj in barcode:
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        barcodeData = obj.data
        barcodeType = obj.type

        with open("output.txt","ab") as file:
            file.write(barcodeData)
            sys.exit()
        
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
while True:
    ret, frame = cap.read()

    decoder(frame)

    cv2.imshow('Image', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break
