import cv2
import base64
import numpy as np
from pyzbar.pyzbar import decode
from qr_lib.helper import decode_img
from PIL import Image


class QrsToFile:
    '''
    This class takes Data from parts of a file
    format is First 4 bytes are index of part of file
    next 4 bytes are how many parts to expect (only exists in first part)
    rest of bytes are just raw data of the file

    usage is intialize the class and call parseFilePart continously until it returns True
    once it returns true you can access full_file_data and file_name for the data of the file
    '''

    def __init__(self) -> None:
        self.already_read = {}
        self.file_parts = 0
        self.full_file_data = b''

    def parseFilePart(self, data) -> bool:
        if(self._get_file_metadata(data) == False):
            self._get_file_data(data)

        if(self.file_parts != 0 and len(self.already_read) == self.file_parts):
            self._build_file_from_parts()
            return True
        else:
            return False

    def _build_file_from_parts(self):
        for key in list(sorted(self.already_read.keys()))[1:]:
            data = self.already_read[key]
            self.full_file_data += data
        self.full_file_data = base64.b64decode(self.full_file_data)

    def _parse_number(self, number):
        return int(number)

    def _write_to_dict(self, index, data):
            if not index in self.already_read:
                print(f'{len(self.already_read) + 1}/{self.file_parts if self.file_parts > 0 else "?"}')
            self.already_read[index] = data

    def _get_file_metadata(self, data):
        number = self._parse_number(data[:4])
        if(number != 0):
            return False
        self.file_parts = int(data[4:8])
        name = data[8:].decode('ascii')
        self._write_to_dict(number,name)
        self.file_name = name

    def _get_file_data(self, data):
        number = self._parse_number(data[:4])
        file_data = data[4:]
        try:
            self.already_read[number]
        except:
            self._write_to_dict(number,file_data)

