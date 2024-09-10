from Newsletter_database.news_api import NewsAPI
from utils.email_service import send_email
from mining_summary.spiders.generatePDF import PDF
import json

class NewsletterSender:
    def __init__(self):
        self.news_api = NewsAPI()
        self.pdf_generator = PDF()

    def prepare_newsletter(self, user_id):
        user = self.news_api.get_user(user_id)
        if not user:
            print(f"User with id {user_id} not found")
            return None

        preferences = json.loads(user['preferences'])
        articles = self.news_api.get_articles_by_categories(preferences['categories'], limit=5)

        text_content = f"Witaj {user['name']},\n\nOto najnowsze artykuły z Twoich ulubionych kategorii:\n\n"
        html_content = f"<h1>Witaj {user['name']},</h1><p>Oto najnowsze artykuły z Twoich ulubionych kategorii:</p>"

        for article in articles:
            text_content += f"Tytuł: {article['title']}\n"
            text_content += f"Streszczenie: {article['summary']}\n"
            text_content += f"Link: {article['link']}\n\n"

            html_content += f"<h2>{article['title']}</h2>"
            html_content += f"<p>{article['summary']}</p>"
            html_content += f"<p><a href='{article['link']}'>Czytaj więcej</a></p>"

        # Generowanie PDF dla każdej kategorii
        pdf_paths = []
        for category in preferences['categories']:
            pdf_path = self.news_api.generate_pdf_by_category(category)
            if pdf_path:
                pdf_paths.append(pdf_path)

        return {
            'text_content': text_content,
            'html_content': html_content,
            'pdf_paths': pdf_paths
        }

    def send_newsletters(self):
        users = self.news_api.get_all_users()
        for user in users:
            content = self.prepare_newsletter(user['id'])
            if content:
                send_email(
                    user['email'],
                    "Twój codzienny newsletter technologiczny",
                    content['text_content'],
                    content['html_content'],
                    content['pdf_paths']
                )

if __name__ == "__main__":
    sender = NewsletterSender()
    sender.send_newsletters()
