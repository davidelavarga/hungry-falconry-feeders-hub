import logging
from datetime import datetime
from typing import Callable

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from utils.get_config import get_config


class ScheduleBuilder(object):

    def __init__(self):
        self.jobstores = {
            'default': MemoryJobStore(),
            'redis': RedisJobStore()
        }
        self.executors = {
            'default': ProcessPoolExecutor(max_workers=get_config()["scheduler"].get("process_pool_max_workers", 20))
        }
        self.job_defaults = {
            'coalesce': True,
            'max_instances': 1
        }
        self.scheduler = BackgroundScheduler(jobstores=self.jobstores,
                                             executors=self.executors,
                                             job_defaults=self.job_defaults)

    def manage_action(self, data: dict, action: str, job: Callable):
        params = (data, job)
        getattr(self, action)(*params)

    def add(self, data, job):
        schedule_id = str(data["id"])
        schedule_date = data["timestamp"]
        feeder_id = data["feeder"]
        run_date = datetime.strptime(schedule_date, "%Y-%m-%dT%H:%M:%SZ")

        self.scheduler.add_job(job, "date", run_date=run_date, id=schedule_id, args=[feeder_id],
                               replace_existing=True)

    def remove(self, data, job):
        try:
            schedule_id = str(data["id"])
            self.scheduler.remove_job(schedule_id)
        except Exception:
            logging.exception(f"Schedule does not exist. Data: {data}")

    def start(self):
        return self.scheduler.start()

    def shutdown(self):
        return self.scheduler.shutdown()

# data = {"id": 22, "action": "add", "timestamp": "2020-12-15T11:28:00Z", "done": True, "feeder": 1}
# data = {"id": 22, "action": "remove", "timestamp": "2020-12-15T11:28:00Z", "done": True, "feeder": 1}
