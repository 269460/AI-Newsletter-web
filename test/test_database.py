from Newsletter_database.news_api import NewsAPI


def test_database():
    news_api = NewsAPI()

    # Test połączenia
    print("Database connected:", news_api.connection.is_connected())

    # Test pobierania kategorii
    categories = news_api.get_categories()
    print("Categories:", categories)

    # Test pobierania artykułów
    articles = news_api.get_articles_by_category("AI")
    print("Number of AI articles:", len(articles))

    # Test wyszukiwania
    search_results = news_api.search_articles("artificial intelligence")
    print("Search results:", len(search_results))


if __name__ == "__main__":
    test_database()