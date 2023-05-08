import csv
import datetime
import os

import pandas
from errors import FormatNameError, write_bad_row_to_file
from loguru import logger
from PMC.schemes import CSVRow

MIN_PARTY: int = 1
DEFAULT_NAME: str = 'Автопринадлежность'


def _formatted_price(price: str) -> int:
    return int(
        float(price.translate(str.maketrans({',': '.', '\xa0': '', ' ': ''})))
    )


def _formatted_party(party: str) -> int:
    return MIN_PARTY if party == '' else int(party)


def _get_now_data() -> str:
    delta8h = datetime.timedelta(hours=8)
    data = datetime.datetime.now(datetime.timezone.utc) + delta8h
    return data.strftime("%d%m%y_%H%M")


class PriceManager:
    '''
        Класс PriceManager используется для парсинга csv файлов из программы Emex.Commerсial,
        изменения цены и формирования файла excel

        Примечание
        ----------
            Проблемы с кодировкой файла csv из Commerсial. Файл нельзя изменять в ручную
            после выгрузки из Commetial. Меняется кодировка и парсинг не возможет. Парсить файл
            строго в кодировке "Windows-1251"

        Атрибуты
        --------
            path_to_file: str
                путь до файла из Emex.Commerсial
            price: list[tuple]
                Сформированный пайс с помощью _get_list_deatails во время создания экземпляра
                из файла по пути path_to_file

        Методы
        ------
            change_price(percent: float, min_price:int)
                Изменяет список price. Устанавливает новую цену. Удаляет детали из списка если
                они не проходят по-ценовому минимуму.

            to_excel(name_file: str, headers: list[str])
                Из списка price формирует excel файл используя библиотеку pandas.
                Так же удаляет рабочий файл csv из Emex.Commetcial
    '''
    def __init__(self, path_to_file: str,) -> None:
        self.path_to_file: str = path_to_file
        self.price: list[tuple] = self._get_list_details(self.path_to_file)

    def _get_list_details(self, path: str) -> list[tuple]:
        '''
            Закрытый метод для парсинга файла, и формирования
            списка price.

            Параметры
            ---------
                path_to_file: str
                    Путь к файлу csv из программы Emex.Commercial

            Примечание
            ----------
                У данного метода не вызывается исключения, только перехватывается
                ValueError когда схема CSVRow формируется для работы с деталями.
                Исключение перехватывается, только в том случае если найдена
                ошибка в преобразовании данных из файла в схему. Такие данные, ввиде
                строки записываются в файл, через write_bad_row_to_file.
        '''
        csvrow: list[tuple] = []
        with open(path, mode='r', encoding='windows-1251') as file:
            file_csv_read = csv.reader(file, delimiter="\t")
            for row_csv in file_csv_read:
                try:
                    row = CSVRow(
                        vendor_code=row_csv[1],
                        name_detail=row_csv[2],
                        quantity=int(row_csv[3]),
                        party=_formatted_party(row_csv[4]),
                        price=_formatted_price(row_csv[5]),
                        manufacturer=row_csv[6],
                    )
                    if row.name_detail == '':
                        row.name_detail = DEFAULT_NAME
                    csvrow.append(row.to_tuple())
                except ValueError as err:
                    write_bad_row_to_file(row_csv, err)
                    continue
        return csvrow

    def change_price(self, percent: float, min_price: int):
        '''
            Метод для изменения цены и корректировки содержимого price

            Параментры
            ----------
                percent: float
                    Процент который передается ввиде числа float.
                    percent перемножается с ценной каждой детали,
                    тем самым устанавливая наценку.
                min_price: int
                    Ограничевающий ценовой минимум. Все что ниже
                    min_price будет удаляться из price
        '''
        for index, row_price in enumerate(self.price):
            row = CSVRow(*row_price)
            if row.price < min_price:
                del self.price[index]
            row.price = int(row.price * percent)

    def to_excel(self, name_file: str, headers: list[str]) -> None:
        '''
            Метод для выгрузки данные из price в файл excel.
            Использует библиотеку pandas

            Параметры
            ---------
                name_file: str
                    Имя будущего excel файла. Обязательно указывается
                    {} двойные скобки, в них будет записана дата
                    формирования файла. Пример: name_file_{<date>}.excel
                headers: list[str]
                    Передаются заголовки для excel файла. Они иду стандартные.
                    "Артикул Наименование Кол-во Партия Цена Производитель"
                    Есть возможность их изменить через конфигурационный файл.

            Исключения
            ----------
            FormatNameError
                В name_file отсутствуют {} две скобки
        '''
        if '{}' not in name_file:
            logger.error('В имени файла для excel отсутствуют {} две скобки')
            raise FormatNameError
        name_to_excel: str = name_file.format(_get_now_data())
        pandas.DataFrame(data=self.price, columns=headers) \
              .to_excel(name_to_excel, index=False, engine='openpyxl')
        os.remove(self.path_to_file)
