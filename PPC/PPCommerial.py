import csv
import datetime
import os

import pandas

from PPC.schemes import CSVRow


MIN_PARTY = 1


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


class PCSVFile:
    def __init__(
        self,
        path_file: str,
        percent: float,
        min_price: int,
        defaut_name: str,
        defaut_header: list,
    ) -> None:
        self.path_file = path_file
        self.percent = percent
        self.min_price = min_price
        self.defaut_name = defaut_name
        self.defaut_header = defaut_header

    def _get_list(self, path: str) -> list[tuple]:
        csvrow: list[tuple] = []
        with open(path) as file:
            csv_read = csv.reader(file, delimiter="\t")
            for row_csv in csv_read:
                row = CSVRow(
                    provider=row_csv[0],
                    vendor_code=row_csv[1],
                    name_detail=row_csv[2],
                    quantity=int(row_csv[3]),
                    party=_formatted_party(row_csv[4]),
                    price=_formatted_price(row_csv[5]),
                    manufacturer=row_csv[6],
                )
                if row.price < self.min_price:
                    continue
                if row.name_detail == '':
                    row.name_detail = self.defaut_name
                row.price = int(row.price * self.percent)
                csvrow.append(row.to_tuple())
        return csvrow

    def to_excel(self, name_file: str) -> None:
        name_to_excel = name_file.format(_get_now_data())
        row_csv = self._get_list(self.path_file)
        pandas.DataFrame(data=row_csv, columns=self.defaut_header).to_excel(name_to_excel, index=False)
        os.remove(self.path_file)
