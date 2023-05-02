from dataclasses import dataclass

import yaml


@dataclass
class Config:
    percent: str
    min_price: str
    defaut_name: str
    defaut_header: str
    format_name_xlsx: str


def setup_config(config_path: str) -> Config:

    with open(config_path, 'r', encoding='utf-8') as f:
        raw_config = yaml.safe_load(f)

        config = Config(
            percent=raw_config['PERCENT'],
            min_price=raw_config['MIN_PRICE'],
            defaut_name=raw_config['DEFAUT_NAME'],
            defaut_header=raw_config['DEFAUT_HEADER'],
            format_name_xlsx=raw_config['FORMAT_NAME_XLSX']
        )

    return config
