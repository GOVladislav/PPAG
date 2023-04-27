class PCSVFile:
    def __init__(self, 
                 path_file, 
                 percent, 
                 min_price,
                 min_party,
                 defaut_name,
                 defaut_header,
                 format_name_xlsx,
                 ) -> None:
        self.path_file = path_file
        self.percent = percent
        self.min_price = min_price,
        self.min_party = min_party,
        self.defaut_name = defaut_name,
        self.defaut_header = defaut_header,
        self.format_name_xlsx = format_name_xlsx