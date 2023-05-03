import csv
import datetime
import os

import pandas

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
    def __init__(self, path_to_file: str,) -> None:
        self.path_to_file: str = path_to_file
        self.price: list[tuple] = self._get_list_details(self.path_to_file)

    def _get_list_details(self, path: str) -> list[tuple]:
        csvrow: list[tuple] = []
        with open(path) as file:
            file_csv_read = csv.reader(file, delimiter="\t")
            for row_csv in file_csv_read:
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
        return csvrow

    def change_price(self, percent: float, min_price: int):
        for index, row_price in enumerate(self.price):
            row = CSVRow(*row_price)
            if row.price < min_price:
                del self.price[index]
            row.price = int(row.price * percent)

    def to_excel(self, name_file: str, headers: list[str]) -> None:
        name_to_excel: str = name_file.format(_get_now_data())
        pandas.DataFrame(data=self.price, columns=headers) \
              .to_excel(name_to_excel, index=False, engine='openpyxl')
        os.remove(self.path_to_file)
