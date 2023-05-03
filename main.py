from loguru import logger

from config import setup_config
from PMC.PMCommerial import PriceManager
from utils import find_csv, find_ymal


def main():
    logger.add('debug.log', format='{time} {level} {message}',
               level='DEBUG', rotation='1 day', compression='zip',
               )

    config = setup_config(find_ymal())

    price = PriceManager(path_to_file=find_csv())
    price.change_price(
        percent=config.percent,
        min_price=config.min_price,
    )
    price.to_excel(
        name_file=config.format_name_xlsx,
        headers=config.defaut_header,
    )


if __name__ == "__main__":
    main()
