import os
import time


def find_ymal():
    listdir = os.listdir()
    for file in listdir:
        if file.find('.yaml') != -1:
            return file
    raise FileNotFoundError


def find_csv():
    listdir = os.listdir()
    for file in listdir:
        if file.find('.csv') != -1:
            return file
    raise FileNotFoundError


def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        total_time = end - start
        print('Время выполнения функции {}: {:.2f} секунд'.format(func.__name__, total_time))
        return result
    return wrapper
