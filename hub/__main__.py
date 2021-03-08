import logging
import time
import sys
import os

from hub.hexagonal_settings import get_settings
from hub.domain.schedule_builder import ScheduleBuilder

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
logging.getLogger().setLevel(logging.INFO)


def serve_job(feeder_id: int):
    get_settings().feeder_job().serve_portion(feeder_id)

def main():
    scheduler = ScheduleBuilder()

    try:
        logging.info("Scheduler start")
        # This already create a thread
        scheduler.start()

        logging.info("Receive schedules start")
        get_settings().backend(scheduler, serve_job).receive_schedules()
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == '__main__':
    main()
