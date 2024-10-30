import feedparser
import requests
from bs4 import BeautifulSoup
from Newsletter_database.news_api import NewsAPI


class ArticleFinder:
    def __init__(self):
        self.news_api = NewsAPI()
        # Lista źródeł RSS do przeszukiwania
        self.rss_feeds = [
            "http://feeds.bbci.co.uk/news/technology/rss.xml",
            "http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
            "https://feeds.feedburner.com/TechCrunch/",
            "https://www.wired.com/feed/rss",
            "https://www.theverge.com/rss/index.xml",
            "https://rss.slashdot.org/Slashdot/slashdotMain",
            "https://www.cnet.com/rss/news/",
            "https://feeds.arstechnica.com/arstechnica/technology-lab",
            "https://www.zdnet.com/news/rss.xml",
            "https://www.computerworld.com/index.rss",
            "https://www.engadget.com/rss.xml",
            "https://www.techmeme.com/feed.xml",
            "https://www.technologyreview.com/topnews.rss",
            "https://www.sciencedaily.com/rss/computers_math.xml",
            "https://www.nature.com/subjects/computer-science.rss",
        ]
        # Lista stron internetowych do scrapowania
        self.websites = [
            "https://techcrunch.com",
            "https://www.theverge.com",
            "https://www.wired.com",
            "https://www.cnet.com",
            "https://arstechnica.com",
            "https://www.zdnet.com",
            "https://www.engadget.com",
            "https://www.techmeme.com",
            "https://www.technologyreview.com",
            "https://www.computerworld.com",
            "https://www.infoworld.com",
            "https://www.venturebeat.com",
            "https://www.gizmodo.com",
            "https://www.digitaltrends.com",
            "https://www.techradar.com",
        ]

    def find_new_articles(self):
        """Główna metoda do znajdowania nowych artykułów"""
        try:
            articles = []
            articles.extend(self._parse_rss_feeds())
            articles.extend(self._scrape_websites())
            return self._filter_new_articles(articles)
        except Exception as e:
            self.logger.error(f"Błąd podczas wyszukiwania artykułów: {str(e)}")
            return []

    def _parse_rss_feeds(self):
        """Metoda do parsowania kanałów RSS"""
        articles = []
        for feed_url in self.rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    if hasattr(entry, "title") and hasattr(entry, "link"):
                        articles.append(
                            {
                                "title": entry.title,
                                "link": entry.link,
                                "source": feed_url,
                            }
                        )
            except Exception as e:
                self.logger.error(f"Błąd podczas parsowania RSS {feed_url}: {str(e)}")
        return articles

    def _scrape_websites(self):
        """Metoda do scrapowania stron internetowych"""
        articles = []
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        for website in self.websites:
            try:
                response = requests.get(website, headers=headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, "html.parser")
                for article in soup.find_all(
                    ["article", "div"], class_=["post", "article", "entry"]
                ):
                    title_elem = article.find(["h1", "h2", "h3"])
                    link_elem = article.find("a")

                    if title_elem and link_elem and link_elem.get("href"):
                        link = link_elem["href"]
                        if not link.startswith("http"):
                            link = website.rstrip("/") + "/" + link.lstrip("/")

                        articles.append(
                            {
                                "title": title_elem.text.strip(),
                                "link": link,
                                "source": website,
                            }
                        )
            except Exception as e:
                self.logger.error(f"Błąd podczas scrapowania {website}: {str(e)}")
        return articles

    def _filter_new_articles(self, articles):
        """
        Filtruje nowe artykuły i sprawdza ich streszczenia
        """
        new_articles = []
        for article in articles:
            try:
                # Sprawdź czy artykuł istnieje
                if not self.news_api.article_exists(article["link"]):
                    new_articles.append(article)
                else:
                    # Sprawdź czy artykuł ma wszystkie potrzebne streszczenia
                    article_id = self.news_api.get_article_id_by_link(article["link"])
                    if article_id:
                        summaries = self.news_api.get_article_summaries(article_id)
                        if not summaries or len(summaries) < 10:  # 10 typów czytelników
                            new_articles.append(article)
            except Exception as e:
                self.logger.error(
                    f"Błąd podczas filtrowania artykułu {article['link']}: {str(e)}"
                )

        return new_articles
