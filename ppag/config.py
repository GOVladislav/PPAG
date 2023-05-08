from dataclasses import dataclass

import yaml


@dataclass
class Config:
    level_logging: str
    percent: float
    min_price: int
    defaut_header: list[str]
    format_name_xlsx: str


def setup_config(config_path: str) -> Config:

    with open(config_path, 'r', encoding='utf-8') as f:
        raw_config = yaml.safe_load(f)

        config = Config(
            level_logging=raw_config['LEVEL_LOGGING'],
            percent=float(raw_config['PERCENT']),
            min_price=int(raw_config['MIN_PRICE']),
            defaut_header=raw_config['DEFAUT_HEADER'].split(),
            format_name_xlsx=raw_config['FORMAT_NAME_XLSX'],
        )
    return config
