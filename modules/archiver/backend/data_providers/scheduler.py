from logging import Logger
import os
import time
from celery import Celery

celery = Celery(
    'data_providers',
    backend='redis://localhost:6379/0', 
    broker="pyamqp://admin:admin@localhost:5672/"
)   

# Logger.info("Autodiscovering tasks...")
# celery.autodiscover_tasks(
#     [
#         # "fides.api.ops.tasks",
#         # "fides.api.ops.tasks.scheduled",
#         # "fides.api.ops.service.privacy_request",
#     ]
# )

@celery.task
def healthbeat(arg):
    print(arg)
    time.sleep(5)
    print("Done")
    return arg

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, healthbeat.s('hello'), name='add every 10')

    # Calls healthbeat('hello') every 30 seconds.
    # It uses the same signature of previous task, an explicit name is
    # defined to avoid this task replacing the previous one defined.
    sender.add_periodic_task(30.0, healthbeat.s('hello'), name='add every 30')

    # Calls healthbeat('world') every 30 seconds
    sender.add_periodic_task(30.0, healthbeat.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Hceleryy Mondays!'),
    # )

# if __name__ == '__main__':
#     celery.start()
# else:
celery.worker_main(
    argv=[
        "worker",
        "--loglevel=debug",
        "--events",
        "--beat",
        f'--concurrency={os.environ.get("CELERY_CONCURRENCY", 2)}'
    ]
)


