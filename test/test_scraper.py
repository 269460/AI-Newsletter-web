from mining_summary.spiders.mining_summary import MiningSpider
from scrapy.crawler import CrawlerProcess


def test_scraper():
    process = CrawlerProcess(settings={
        'LOG_LEVEL': 'INFO',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    })

    process.crawl(MiningSpider)
    process.start()


if __name__ == "__main__":
    test_scraper()