from Newsletter_database.news_api import NewsAPI


class PDF:
    def __init__(self):
        self.news_api = NewsAPI()

    def generate_pdfs(self, categories):
        """
        Generuje PDF-y dla podanych kategorii.

        :param categories: Lista kategorii, dla których mają być wygenerowane PDF-y
        """
        for category in categories:
            self.news_api.generate_pdf_by_category(category)
        self.news_api.close()


if __name__ == "__main__":
    pdf_generator = PDF()
    # Generowanie PDF-ów dla wszystkich nowych kategorii
    pdf_generator.generate_pdfs([
        "AI", "IoT", "CS", "RA", "TC",
        "TM", "BT", "NT", "EO", "TK"
    ])