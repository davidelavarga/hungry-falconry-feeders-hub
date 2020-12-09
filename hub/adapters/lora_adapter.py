import requests

from hub.domain.ports import FeederJobPort


class LoraFeederJob(FeederJobPort):

    def __init__(self):
        self.url = ""

    def serve_portion(self, feeder_id: int):
        print(f"Post to {feeder_id}")
        # requests.post(self.url, data=feeder_id)
