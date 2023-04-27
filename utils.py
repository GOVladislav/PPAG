import os

def find_ymal():
    listdir = os.listdir()
    for file in listdir:
        if file.find('.yaml') != -1:
            return file
    raise FileNotFoundError