from loguru import logger

from config import setup_config
from PMC.PMCommerсial import PriceManager
from utils import find_csv, find_ymal


def main():
    config = setup_config(find_ymal())

    logger.add(
        'debug.log', format='{time} {level} {exception} {message}',
        level=config.level_logging, rotation='1 week', compression='zip',
    )

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
