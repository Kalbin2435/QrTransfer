from qr_lib import FileToQr 
import argparse
from qr_lib.QrToFile import QrsToFile
import cv2
import numpy as np
from pyzbar.pyzbar import decode
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
        if(QrToFileHandler.parseFilePart(barcodeData)):
                with open(QrToFileHandler.file_name,"wb") as file:
                    file.write(QrToFileHandler.full_file_data)
                sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--filepath", default="None")
    args = parser.parse_args()
    if args.filepath=="None":
        QrToFileHandler = QrsToFile()
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        while True:
            ret, frame = cap.read()

            decoder(frame)

            cv2.imshow('Image', frame)
            code = cv2.waitKey(10)
            if code == ord('q'):
                break
    else:
        res = FileToQr.translateFileToQrs(args.filepath)




        
        


