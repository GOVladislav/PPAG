from config import setup_config
from PPC.PPCommerial import PCSVFile
from utils import find_ymal, find_csv


def main():
    config = setup_config(find_ymal())
    
    csv_file = PCSVFile(
        path_file=find_csv(),
        percent=float(config.percent),
        min_price=int(config.min_price),
        min_party=int(config.min_party),
        defaut_name=config.defaut_name,
        defaut_header=config.defaut_header,
        format_name_xlsx=config.format_name_xlsx,
        )
    print(csv_file.percent)

if __name__ == "__main__":
    main()