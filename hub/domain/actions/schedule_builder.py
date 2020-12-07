import asyncio
import time
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import utc

jobstores = {
    # 'redis': RedisJobStore()
}
executors = {
    'default': ThreadPoolExecutor(max_workers=20),
    'processpool': ProcessPoolExecutor(max_workers=5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}


def my_job(a):
    print("Hi")
    print(a)
    # Este enviara una request a lora o al adaptador para el actuador


scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

scheduler.add_job(my_job, "date", run_date=datetime(2020, 12, 7, 13, 15), id="1", args=["world1"],
                  replace_existing=True)
scheduler.add_job(my_job, "date", run_date=datetime(2020, 12, 7, 13, 16), id="2", args=["world2"],
                  replace_existing=True)

scheduler.start()
print("Ctrl+c to exit")
try:
    asyncio.get_event_loop().run_forever()
except (KeyboardInterrupt, SystemExit):
    pass
