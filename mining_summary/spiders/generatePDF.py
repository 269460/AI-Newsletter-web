from Newsletter_database.news_api import NewsAPI

class PDF:
    def __init__(self):
        self.news_api = NewsAPI()

    def generate_pdfs(self, categories):
        for category in categories:
            self.news_api.generate_pdf_by_category(category)
        self.news_api.close()

if __name__ == "__main__":
    pdf_generator = PDF()
    pdf_generator.generate_pdfs(["R", "FOCM"])