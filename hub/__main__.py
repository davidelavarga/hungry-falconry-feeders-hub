import logging
import threading
import time

from hexagonal_settings import get_settings
from hub.domain.schedule_builder import ScheduleBuilder


def serve_job(feeder_id: int):
    get_settings().feeder_job().serve_portion(feeder_id)


def main():
    scheduler = ScheduleBuilder()
    scheduler.initialize_scheduler()

    t = threading.Thread(target=get_settings().backend(scheduler, serve_job).receive_schedules)

    try:
        logging.info("Scheduler start")
        # This already create a thread
        scheduler.start()

        logging.info("Receive schedules start")
        t.start()
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == '__main__':
    main()
