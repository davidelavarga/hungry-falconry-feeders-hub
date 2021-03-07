from hub.domain.ports import FeederJobPort
import RPi.GPIO as GPIO
import time

PIN = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)

class LedFeederJob(FeederJobPort):    
    def serve_portion(self, feeder_id: int):
        GPIO.output(PIN, True)
        time.sleep(1)
        GPIO.output(PIN, False)