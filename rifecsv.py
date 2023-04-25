import argparse
import os
import csv
import pandas
import datetime
import logging

from dotenv import load_dotenv
from dataclasses import dataclass


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, filename=f'{__name__}.log', 
                    filemode='a', format='%(asctime)s %(levelname)s %(message)s')


@dataclass
class Row:
    provider: str
    vendor_code: str
    name_detail: str
    quantity: str
    party: str
    price: str
    manufacturer: str

    def to_list(self):
        return [self.vendor_code, self.name_detail, self.quantity, self.party, self.price, self.manufacturer]
    
    def formatted_prise(self):
        price = self.price.replace(',', '.').replace('\xa0', '').replace(' ', '')
        return float(price)
    

def setup_argparametr(config):
    parser = argparse.ArgumentParser(description='Excel file handler')
    parser.add_argument('-p', '--percent', type=float, default=float(config['PERCENT']), help='setup percent in price')
    parser.add_argument('-mp', '--minprice', type=int, default=int(config['MIN_PRICE']), help='setup min price')
    parser.add_argument('-v', '--version', type=str, default='1.1.0', help='Version program')
    parser.add_argument('-z', action='store_true')
    return parser.parse_args()


def setup_config():
    load_dotenv()
    config = {}
    for key in os.environ:
        config.update({key: os.environ[key]})
    return config


def get_now_data():
    delta8h = datetime.timedelta(hours=8)
    data = datetime.datetime.now(datetime.timezone.utc) + delta8h
    return data.strftime("%d%m%y_%H%M")
    


def find_file_cvs():
    listdir = os.listdir()
    for file in listdir:
        if file.find('.csv') != -1:
            return file
    raise FileNotFoundError


def main():
    config = setup_config()
    parametrs = setup_argparametr(config)

    try:
        work_file = find_file_cvs()
    except FileNotFoundError as ex:
        logging.error("Work file cvs: FileNotFoundError") #, exc_info=True) Если хочу трайсбэк увидеть
        raise SystemExit(1)

    with open(work_file) as file_read:
        with open(config['TEMPORARY_NAME_CSV_FILE'], mode='w', encoding='utf-8-sig') as file_write:

            file_csv_read = csv.reader(file_read, delimiter = "\t")
            file_csv_write = csv.writer(file_write, delimiter='\t', lineterminator='\r')

            file_csv_write.writerow(config['DEFAUT_HEADER'].split())

            #TODO Ветвление цикла не правильное
            for row in file_csv_read:
                row = Row(*row)
                formatted_price = row.formatted_prise()
                if formatted_price > int(config['MIN_PRICE']):
                    if row.name_detail == '':
                        row.name_detail = config['DEFAUT_NAME']
                    if row.party == '':
                        row.party = int(config['MIN_PARTY'])
                    row.price = int(formatted_price * parametrs.percent)
                    del row.provider
                    file_csv_write.writerow(row.to_list())


    name_to_excel = config['FORMAT_NAME_EXSPORT_XLSX'].format(get_now_data())
    
    praise = pandas.read_csv(config['TEMPORARY_NAME_CSV_FILE'], sep='\t')
    praise.to_excel(name_to_excel, index=False)

    os.remove(config['TEMPORARY_NAME_CSV_FILE'])
    os.remove(work_file)


if __name__ == "__main__":
    main()