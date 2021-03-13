import logging
import time

import RPi.GPIO as GPIO
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

        self.success_led = 13
        self.fail_led = 26
        self.warn_led = 19
        self.__setup_leds()

    def serve_portion(self, feeder_id: int):
        logging.info(f"Post to {feeder_id}")
        try:
            GPIO.output(self.success_led, True)
            self.rfm9x.send(bytes(f"{feeder_id} {self.serve_action}", "utf-8"))
            logging.info(f"Sent LoRa message successfully!")
            time.sleep(2)
            GPIO.output(self.success_led, False)

        except Exception:
            GPIO.output(self.fail_led, True)
            logging.exception("Error sending serve job!")
            time.sleep(2)
            GPIO.output(self.fail_led, False)

    def __setup_leds(self):
        # Setup
        GPIO.setup(self.success_led, GPIO.OUT)
        GPIO.setup(self.fail_led, GPIO.OUT)
        GPIO.setup(self.warn_led, GPIO.OUT)
