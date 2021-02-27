import logging
import os
from functools import lru_cache

import yaml


def get_config(path: str = ""):
    if not path:
        path = os.environ["CONFIG_PATH"]
    with open(path, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            logging.exception(e)
