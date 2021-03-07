from hub.domain.ports import FeederJobPort
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

class LedFeederJob(FeederJobPort):    
    def serve_portion(self, feeder_id: int):
        GPIO.output(7, True)
        time.sleep(1)
        GPIO.output(7, False)