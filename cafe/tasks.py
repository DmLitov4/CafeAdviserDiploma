from celery.task import periodic_task
from datetime import timedelta
from celery.schedules import crontab
from datetime import timedelta
from login.views import *

@periodic_task(run_every= timedelta(seconds = 20000))
def update_vk_data():
    print("starting vk data update...")
    update_vk_clasters()