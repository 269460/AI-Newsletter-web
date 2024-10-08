from app import db
from app.models import User, Article, Summary
from app.email_sender import send_newsletter
from app.utils import generate_pdf_by_category
import json

class NewsletterSender:
    def __init__(self):
        pass

    def prepare_newsletter(self, user_id):
        user = User.query.get(user_id)
        if not user:
            print(f"User with id {user_id} not found")
            return None

        preferences = json.loads(user.preferences) if user.preferences else {}
        articles = Article.query.join(Summary).filter(
            Summary.category.in_(preferences.get('categories', []))
        ).order_by(Article.created_at.desc()).limit(5).all()

        text_content = f"Hello {user.email},\n\nHere are the latest articles from your favorite categories:\n\n"
        html_content = f"<h1>Hello {user.email},</h1><p>Here are the latest articles from your favorite categories:</p>"

        for article in articles:
            text_content += f"Title: {article.title}\n"
            text_content += f"Summary: {article.summary.summary}\n"
            text_content += f"Link: {article.link}\n\n"

            html_content += f"<h2>{article.title}</h2>"
            html_content += f"<p>{article.summary.summary}</p>"
            html_content += f"<p><a href='{article.link}'>Read more</a></p>"

        # Generate PDF for each category
        pdf_paths = []
        for category in preferences.get('categories', []):
            pdf_path = generate_pdf_by_category(category)
            if pdf_path:
                pdf_paths.append(pdf_path)

        return {
            'user': user,
            'articles': articles,
            'text_content': text_content,
            'html_content': html_content,
            'pdf_paths': pdf_paths
        }

    def send_newsletters(self):
        users = User.query.all()
        for user in users:
            content = self.prepare_newsletter(user.id)
            if content:
                if isinstance(self.send_email, send_newsletter_flask):
                    self.send_email(user, content['context']['articles'])
                else:
                    self.send_email(
                        to_email=user.email,
                        subject="Your technology newsletter",
                        template='email/newsletter',
                        template_context=content['context'],
                        attachments=content['pdf_paths']
                    )

if __name__ == "__main__":
    sender = NewsletterSender()
    sender.send_newsletters()
