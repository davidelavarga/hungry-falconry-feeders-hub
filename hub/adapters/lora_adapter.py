import requests
import logging

from hub.domain.ports import FeederJobPort


class LoraFeederJob(FeederJobPort):

    def __init__(self):
        self.url = ""

    def serve_portion(self, feeder_id: int):
        logging.info(f"Post to {feeder_id}")
        logging.info(f"Successfully!")
        # requests.post(self.url, data=feeder_id)
