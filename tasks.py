from celery import Celery
from mining_summary.spiders.mining_summary import run_spider
from celery.schedules import crontab

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def run_spider_task():
    run_spider()

# Konfiguracja harmonogramu
celery.conf.beat_schedule = {
    'run-spider-every-day': {
        'task': 'tasks.run_spider_task',
        'schedule': crontab(hour=0, minute=0),
    },
}