import logging

from hub.domain.ports import FeederJobPort
from utils.get_config import get_config


class LoraFeederJob(FeederJobPort):
    def __init__(self):
        import adafruit_rfm9x
        import board
        import busio
        from digitalio import DigitalInOut
        cs = DigitalInOut(board.CE1)
        reset = DigitalInOut(board.D25)
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        self.__config = get_config()["lora"]
        self.__actions = self.__config["actions"]
        self.rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, self.__config["frecuency"])
        self.serve_action = self.__actions["serve"]

    def serve_portion(self, feeder_id: int):
        logging.info(f"Post to {feeder_id}")
        try:
            self.rfm9x.send(bytes(f"{feeder_id} {self.serve_action}", "utf-8"))
            logging.info(f"Successfully!")

        except Exception:
            logging.exception("Error sending serve job!")
