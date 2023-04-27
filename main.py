from config import setup_config
from PPC.PPCommerial import PCSVFile
from utils import find_ymal


def main():
    config = setup_config(find_ymal())
    

if __name__ == "__main__":
    main()