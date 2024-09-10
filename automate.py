import schedule
import time
from mining_summary.spiders.mining_summary import run_spider
from Newsletter_database.news_api import NewsAPI

def job():
    print("Running spider...")
    run_spider()
    print("Spider finished. Updating summaries...")
    news_api = NewsAPI()
    news_api.update_summaries()
    print("Job completed.")

schedule.every().day.at("00:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)