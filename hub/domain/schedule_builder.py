import asyncio
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from pytz import utc

from hexagonal_settings import get_settings


class ScheduleBuilder(object):

    def __init__(self):
        self.jobstores = {
            # 'redis': RedisJobStore()
        }
        self.executors = {
            'default': ThreadPoolExecutor(max_workers=20),
            'processpool': ProcessPoolExecutor(max_workers=5)
        }
        self.job_defaults = {
            'coalesce': False,
            'max_instances': 3  # TODO max portions????
        }
        self.scheduler = None

    def initialize_scheduler(self):
        self.scheduler = AsyncIOScheduler(jobstores=self.jobstores,
                                          executors=self.executors,
                                          job_defaults=self.job_defaults,
                                          timezone=utc)

    def feeder_schedule_as_job(self, data: dict):
        schedule_id = str(data["id"])
        schedule_date = data["timestamp"]
        feeder_id = data["feeder"]
        run_date = datetime.strptime(schedule_date, "%Y-%m-%dT%H:%M:%SZ")

        job = get_settings().feeder_job().serve_portion

        self.scheduler.add_job(job, "date", run_date=run_date, id=schedule_id, args=[feeder_id],
                               replace_existing=True)

    def start(self):
        self.scheduler.start()
        try:
            asyncio.get_event_loop().run_forever()
        except (KeyboardInterrupt, SystemExit) as e:
            print(e)

# data = {"id": 22, "timestamp": "2020-12-15T11:28:00Z", "done": True, "feeder": 1}
