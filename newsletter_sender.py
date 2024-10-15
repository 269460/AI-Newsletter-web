from app import mail
from Newsletter_database.news_api import NewsAPI
from flask_mail import Message
from flask import render_template
import json

class NewsletterSender:
    def __init__(self):
        self.news_api = NewsAPI()

    def prepare_newsletter(self, user):
        preferences = json.loads(user['preferences']) if user['preferences'] else {}
        articles = self.news_api.get_articles_by_categories(preferences.get('categories', []), limit=5)

        content = {
            'user': user,
            'articles': articles,
            'pdf_path': self.news_api.generate_pdf_by_category(preferences.get('categories', []))
        }

        return content

    def send_newsletter(self, content):
        msg = Message('Your AI Newsletter',
                      sender='noreply@ainewsletter.com',
                      recipients=[content['user']['email']])
        msg.body = render_template('email/newsletter.txt', user=content['user'], articles=content['articles'])
        msg.html = render_template('email/newsletter.html', user=content['user'], articles=content['articles'])

        if content['pdf_path']:
            with open(content['pdf_path'], 'rb') as pdf:
                msg.attach("newsletter.pdf", 'application/pdf', pdf.read())

        mail.send(msg)

    def send_newsletters(self):
        subscribed_users = self.news_api.get_subscribed_users()
        for user in subscribed_users:
            content = self.prepare_newsletter(user)
            self.send_newsletter(content)

if __name__ == "__main__":
    sender = NewsletterSender()
    sender.send_newsletters()