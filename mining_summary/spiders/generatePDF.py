from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
from app.models import Article, Category
from app import db

class PDF:
    def __init__(self):
        self.styles = getSampleStyleSheet()

    def generate_pdf_by_category(self, category_name):
        """
        Generuje PDF dla podanej kategorii.

        :param category_name: Nazwa kategorii
        :return: Ścieżka do wygenerowanego pliku PDF
        """
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            print(f"Category {category_name} not found")
            return None

        articles = Article.query.filter_by(category=category).order_by(Article.created_at.desc()).limit(10).all()

        if not articles:
            print(f"No articles found for category {category_name}")
            return None

        pdf_filename = os.path.join(os.getcwd(), f"{category_name}_newsletter.pdf")
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        story = []

        story.append(Paragraph(f"Newsletter: {category_name}", self.styles['Title']))
        story.append(Spacer(1, 12))

        for article in articles:
            story.append(Paragraph(article.title, self.styles['Heading2']))
            if article.summary:
                story.append(Paragraph(article.summary.summary, self.styles['BodyText']))
            story.append(Paragraph(f"Link: {article.link}", self.styles['BodyText']))
            story.append(Spacer(1, 12))

        doc.build(story)
        print(f"PDF generated: {pdf_filename}")
        return pdf_filename

    def generate_pdfs(self, categories):
        """
        Generuje PDF-y dla podanych kategorii.

        :param categories: Lista kategorii, dla których mają być wygenerowane PDF-y
        """
        for category in categories:
            self.generate_pdf_by_category(category)


if __name__ == "__main__":
    pdf_generator = PDF()
    # Generowanie PDF-ów dla wszystkich kategorii
    categories = [cat.name for cat in Category.query.all()]
    pdf_generator.generate_pdfs(categories)