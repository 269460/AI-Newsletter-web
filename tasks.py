# Aby uruchomić Celery:
# Uruchom workera: celery -A tasks worker --loglevel=info
# Uruchom beat (dla zadań cyklicznych): celery -A tasks beat --loglevel=info
from celery import Celery
from celery.schedules import crontab

from mining_summary.spiders.mining_summary import run_spider
from Newsletter_database.news_api import NewsAPI
from newsletter_sender import NewsletterSender

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def update_articles():
    run_spider()

@celery.task
def update_summaries():
    news_api = NewsAPI()
    news_api.update_summaries()

@celery.task
def send_newsletters():
    sender = NewsletterSender()
    sender.send_newsletters()

@celery.task
def automated_update_and_send():
    update_articles.delay()
    update_summaries.delay()
    send_newsletters.delay()

# Konfiguracja harmonogramu
celery.conf.beat_schedule = {
    'run-daily-update': {
        'task': 'tasks.automated_update_and_send',
        'schedule': crontab(hour=0, minute=0),  # Uruchamia codziennie o północy
    },
}