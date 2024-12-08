import base64
import os
from datetime import datetime
import qrcode
from qrcode.util import QRData
from qrcode.util import MODE_8BIT_BYTE


def translateFileToQrs(path):
    _make_data_directory(path)
    with open(path, "rb") as file:
        data = file.read()
        ascii_bytes = base64.b64encode(data)
        _createImagesFromData(ascii_bytes)

    number = _number_to_padded_byte_number(0)
    filename = bytes(os.path.basename(path), "ascii")
    file_counter = _get_file_count()
    file_count = _number_to_padded_byte_number(file_counter)
    first_qr_data = number + file_count + filename
    qrcodeMakeImage(first_qr_data,"0.png")

def qrcodeMakeImage(data,path):
    qr = qrcode.QRCode(version=None,
                       error_correction=qrcode.ERROR_CORRECT_L,
                       box_size=10,
                       border=4
                       )
    # def __init__(self, data, mode=None, check_data=True):
    qr.add_data(data,optimize=0)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(path)

def _get_file_count():
    cwd = os.getcwd()
    file_count = sum(1 for entry in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, entry)))
    return file_count + 1 # + 1 for including the last image, added after


def _make_data_directory(path):
    filename_no_ext = os.path.splitext(os.path.basename(path))
    dirname = "qr_data_" + filename_no_ext[0] + "_" + _get_file_writable_date()
    os.mkdir(dirname)
    os.chdir(dirname)

def _number_to_padded_byte_number(number, digits=4):
    number = f'{number:0{digits}}'
    number = bytes(number, "ascii")
    return number

def _createImagesFromData(data, bytes_per_images=2900):
    index = 1
    if(len(data) >= bytes_per_images):
        qrcodeMakeImage(_number_to_padded_byte_number(index) + data[:bytes_per_images], str(index) + ".png")
        index += 1
        data = data[bytes_per_images:]

    while(len(data) >= bytes_per_images):
        qrcodeMakeImage(_number_to_padded_byte_number(index) + data[:bytes_per_images],str(index) + ".png")
        data = data[bytes_per_images:]
        index += 1

    if(len(data) >= 0):
        qrcodeMakeImage(_number_to_padded_byte_number(index) + data,str(index) + ".png")

def _get_file_writable_date():
    current_date = datetime.now()
    formatted_Date = current_date.strftime("%Y-%m-%d_%H-%M-%S")
    return formatted_Date
