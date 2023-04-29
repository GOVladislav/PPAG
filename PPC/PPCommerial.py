import csv
import datetime
import os

import pandas

from PPC.model import CSVRow


class PCSVFile:
    def __init__(self,
                 path_file: str,
                 percent: float,
                 min_price: int,
                 min_party: int,
                 defaut_name: str,
                 defaut_header: list,
                 format_name_xlsx: str,
                 ) -> None:
        self.path_file = path_file
        self.percent = percent
        self.min_price = min_price
        self.min_party = min_party
        self.defaut_name = defaut_name
        self.defaut_header = defaut_header
        self.format_name_xlsx = format_name_xlsx

    def _get_now_data(self) -> str:
        delta8h = datetime.timedelta(hours=8)
        data = datetime.datetime.now(datetime.timezone.utc) + delta8h
        return data.strftime("%d%m%y_%H%M")

    def to_excel(self) -> None:
        with open(self.path_file) as file_read:
            with open('_.csv', mode='w', encoding='utf-8-sig') as file_write:

                file_csv_read = csv.reader(file_read, delimiter="\t")
                file_csv_write = csv.writer(file_write, delimiter='\t', lineterminator='\r')

                file_csv_write.writerow(self.defaut_header)

                for row in file_csv_read:
                    row = CSVRow(*row)
                    formatted_price = row.formatted_price()
                    if formatted_price < self.min_price:
                        continue
                    if row.name_detail == '':
                        row.name_detail = self.defaut_name
                    if row.party == '':
                        row.party = self.min_party
                    row.price = int(formatted_price * self.percent)
                    del row.provider
                    file_csv_write.writerow(row.to_list())

        name_to_excel = self.format_name_xlsx.format(self._get_now_data())
        praise = pandas.read_csv('_.csv', sep='\t')
        praise.to_excel(name_to_excel, index=False)

        os.remove('_.csv')
        os.remove(self.path_file)
