import yaml
from loguru import logger
from pydantic import BaseModel, StrictFloat, StrictInt, ValidationError

from errors import headling_error_pydantic


class Config(BaseModel):
    percent: StrictFloat
    min_price: StrictInt
    defaut_header: list[str]
    format_name_xlsx: str


def setup_config(config_path: str) -> Config:

    with open(config_path, 'r', encoding='utf-8') as f:
        raw_config = yaml.safe_load(f)

        try:
            config = Config(
                percent=raw_config['PERCENT'],
                min_price=raw_config['MIN_PRICE'],
                defaut_header=raw_config['DEFAUT_HEADER'].split(),
                format_name_xlsx=raw_config['FORMAT_NAME_XLSX'],
            )
        except ValidationError as e:
            logger.error(headling_error_pydantic(e.errors()))
            raise SystemExit(1)
    return config
