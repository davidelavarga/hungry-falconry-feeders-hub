from hexagonal_settings import get_settings
from hub.domain.schedule_builder import ScheduleBuilder

if __name__ == '__main__':
    scheduler = ScheduleBuilder()
    scheduler.initialize_scheduler()
    # TODO in a thread
    get_settings().backend(scheduler).receive_schedules()
    # TODO in another thread
    scheduler.start()
