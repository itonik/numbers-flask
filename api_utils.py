import socket
import time
import random
from os import listdir
from os.path import isfile, join
import qrcode

# Time as "Fri Nov 15 21:59:22 2019" string
def get_time_string():
    return time.ctime(time.time()).replace(' ','-')

# Random number between 1000 and 9999
def get_random_number_string():
    return str(random.randint(1000,9999))

# Makes names for uploaded files
def fancy_filename(user_filename):
    file_extension = user_filename.split('.')[-1]
    if file_extension == None:
        raise Exception('File does not have an extension')
    return '{0}-{1}.{2}'.format(get_time_string(), get_random_number_string(), file_extension)

def get_files_in_directory():
    path = 'uploads'
    return [f for f in listdir(path) if isfile(join(path, f)) and f[0] != '.']

def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

def make_qr():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=14,
        border=4,
    )
    qr.add_data('http://{0}:5000'.format(get_local_ip()))
    qr.make(fit=True)
    img = qr.make_image()
    img.save('qr_last.png')