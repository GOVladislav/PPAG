from config import setup_config
from PPC.PPCommerial import PCSVFile
from utils import find_ymal, find_csv


def main():
    config = setup_config(find_ymal())
    
    csv_file = PCSVFile(
        path_file=find_csv(),
        percent=config.percent,
        min_price=config.min_price,
        min_party=config.min_party,
        defaut_name=config.defaut_name,
        defaut_header=config.defaut_header.split(),
        format_name_xlsx=config.format_name_xlsx,
        )


if __name__ == "__main__":
    main()