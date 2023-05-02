from loguru import logger

from config import setup_config
from PPC.PPCommerial import PCSVFile
from utils import find_csv, find_ymal


def main():
    logger.add('debug.log', format='{time} {level} {message}',
               level='DEBUG', rotation='1 day', compression='zip',
               )

    config = setup_config(find_ymal())

    csv_file = PCSVFile(
        path_file=find_csv(),
        percent=float(config.percent),
        min_price=int(config.min_price),
        defaut_name=config.defaut_name,
        defaut_header=config.defaut_header.split(),
    )
    csv_file.to_excel(name_file=config.format_name_xlsx)


if __name__ == "__main__":
    main()
