import os
import time

from loguru import logger


def find_yaml() -> str:
    '''
        Функция ищит файл с расширением .yaml

        Исключения
        ----------
        FileNotFoundError
            Вызывается когда файл с расширением .yaml не найден
    '''
    listdir = os.listdir()
    for file in listdir:
        if file.find('.yaml') != -1:
            return file
    logger.error('Файл конфигурации(cofig.yaml) не может быть найден или открыт')
    raise FileNotFoundError


def find_csv() -> str:
    '''
        Функция ищит файл с расширением .csv

        Исключения
        ----------
        FileNotFoundError
            Вызывается когда файл с расширением .csv не найден
    '''
    listdir = os.listdir()
    for file in listdir:
        if file.find('.csv') != -1:
            return file
    logger.error('Файл прайс csv не может быть найден или открыт')
    raise FileNotFoundError


def _time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        total_time = end - start
        print('Время выполнения функции {}: {:.2f} секунд'.format(func.__name__, total_time))
        return result
    return wrapper
