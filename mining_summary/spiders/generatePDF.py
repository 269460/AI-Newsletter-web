from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os
from sqlalchemy.testing.plugin.plugin_base import logging
from Newsletter_database.news_api import NewsAPI
from app.models import Article, Category


class PDF:
    """
    Klasa odpowiedzialna za generowanie newsletterów w formacie PDF.
    Łączy funkcjonalności pobierania danych z API i generowania PDF.
    """

    def __init__(self):
        self.news_api = NewsAPI()
        self.logger = logging.getLogger(__name__)
        self.styles = self._create_styles()

    def _create_styles(self):
        """
        Tworzy i konfiguruje style dla dokumentu PDF.
        """
        styles = getSampleStyleSheet()

        # Dodanie własnych stylów
        styles.add(
            ParagraphStyle(
                name="CategoryHeader",
                parent=styles["Title"],
                fontSize=24,
                spaceAfter=30,
                textColor=colors.HexColor("#1a73e8"),
            )
        )

        styles.add(
            ParagraphStyle(
                name="ArticleTitle",
                parent=styles["Heading2"],
                fontSize=16,
                spaceAfter=10,
                textColor=colors.HexColor("#202124"),
            )
        )

        styles.add(
            ParagraphStyle(
                name="Summary",
                parent=styles["BodyText"],
                fontSize=12,
                spaceAfter=8,
                leading=14,
            )
        )

        styles.add(
            ParagraphStyle(
                name="Link",
                parent=styles["BodyText"],
                fontSize=10,
                textColor=colors.blue,
                spaceAfter=20,
            )
        )

        return styles

    def generate_newsletter(self, category):
        """
        Generuje newsletter dla pojedynczej kategorii.

        Args:
            category (str): Nazwa kategorii

        Returns:
            str: Ścieżka do wygenerowanego pliku PDF lub None w przypadku błędu
        """
        try:
            # Pobierz artykuły dla kategorii
            articles = self.news_api.get_articles_by_categories([category])
            if not articles:
                self.logger.warning(f"Brak artykułów dla kategorii {category}")
                return None

            # Przygotuj nazwę pliku
            date_str = datetime.now().strftime("%Y%m%d")
            pdf_filename = os.path.join(
                os.getcwd(), "newsletters", f"{category}_{date_str}_newsletter.pdf"
            )

            # Upewnij się, że katalog istnieje
            os.makedirs(os.path.dirname(pdf_filename), exist_ok=True)

            # Utwórz dokument
            doc = SimpleDocTemplate(
                pdf_filename,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72,
            )

            # Przygotuj zawartość
            story = self._create_newsletter_content(category, articles)

            # Zbuduj PDF
            doc.build(story)
            self.logger.info(
                f"Wygenerowano newsletter dla kategorii {category}: {pdf_filename}"
            )
            return pdf_filename

        except Exception as e:
            self.logger.error(
                f"Błąd podczas generowania newslettera dla {category}: {str(e)}"
            )
            return None

    def _create_newsletter_content(self, category, articles):
        """
        Tworzy zawartość newslettera.

        Args:
            category (str): Nazwa kategorii
            articles (list): Lista artykułów

        Returns:
            list: Lista elementów do umieszczenia w PDF
        """
        story = []

        # Nagłówek newslettera
        date_str = datetime.now().strftime("%d.%m.%Y")
        story.append(
            Paragraph(
                f"{category} Tech Newsletter - {date_str}",
                self.styles["CategoryHeader"],
            )
        )
        story.append(Spacer(1, 20))

        # Dodaj artykuły
        for article in articles:
            # Pobierz streszczenia dla artykułu
            summaries = self.news_api.get_article_summaries(article["id"])

            # Dodaj tytuł artykułu
            story.append(Paragraph(article["title"], self.styles["ArticleTitle"]))

            # Dodaj streszczenia
            if summaries:
                for summary in summaries:
                    reader_type = summary["reader_type"]
                    summary_text = summary["summary"]

                    if summary_text and summary_text != "not enough info":
                        story.append(
                            Paragraph(
                                f"<b>{reader_type} perspective:</b>",
                                self.styles["Summary"],
                            )
                        )
                        story.append(Paragraph(summary_text, self.styles["Summary"]))
                        story.append(Spacer(1, 10))

            # Dodaj link do artykułu
            story.append(
                Paragraph(f"Read more: {article['link']}", self.styles["Link"])
            )
            story.append(Spacer(1, 20))

        return story

    def generate_all_newsletters(self):
        """
        Generuje newslettery dla wszystkich kategorii.

        Returns:
            dict: Słownik z wynikami generowania {kategoria: ścieżka_do_pdf}
        """
        categories = ["AI", "IoT", "CS", "RA", "TC", "TM", "BT", "NT", "EO", "TK"]
        results = {}

        for category in categories:
            pdf_path = self.generate_newsletter(category)
            results[category] = pdf_path

            if pdf_path:
                self.logger.info(f"Newsletter dla {category} wygenerowany: {pdf_path}")
            else:
                self.logger.error(
                    f"Nie udało się wygenerować newslettera dla {category}"
                )

        return results


def main():
    """
    Główna funkcja do uruchamiania generatora newsletterów.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    generator = PDF()
    results = generator.generate_all_newsletters()

    # Wyświetl podsumowanie
    success = len([p for p in results.values() if p is not None])
    total = len(results)
    print(f"\nWygenerowano {success}/{total} newsletterów")


if __name__ == "__main__":
    main()
