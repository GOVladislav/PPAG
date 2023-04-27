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
        self.min_price = min_price,
        self.min_party = min_party,
        self.defaut_name = defaut_name,
        self.defaut_header = defaut_header,
        self.format_name_xlsx = format_name_xlsx