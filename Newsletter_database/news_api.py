import json
import mysql.connector
from mysql.connector import Error
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

class NewsAPI:
    def __init__(self):
        self.connection = self.connect()
        if self.connection is None:
            raise Exception("Failed to connect to the database")

    def connect(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='newsletter',
                password='newsletter',
                database='newsletter'
            )
            print("Connected to MySQL database")
            return connection
        except Error as e:
            self.logger.error(f"Error connecting to MySQL database: {e}")
            return None

    def subscribe_user(self, user_id):
        cursor = self.connection.cursor()
        query = "UPDATE users SET is_subscribed = TRUE WHERE id = %s"
        try:
            cursor.execute(query, (user_id,))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error subscribing user {user_id}: {e}")
            return False
        finally:
            cursor.close()

    def unsubscribe_user(self, user_id):
        cursor = self.connection.cursor()
        query = "UPDATE users SET is_subscribed = FALSE WHERE id = %s"
        try:
            cursor.execute(query, (user_id,))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error unsubscribing user {user_id}: {e}")
            return False
        finally:
            cursor.close()

    def is_user_subscribed(self, user_id):
        cursor = self.connection.cursor()
        query = "SELECT is_subscribed FROM users WHERE id = %s"
        try:
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            return result[0] if result else False
        except Error as e:
            print(f"Error checking subscription status for user {user_id}: {e}")
            return False
        finally:
            cursor.close()

    def get_articles_by_categories(self, categories, limit=5):
        cursor = self.connection.cursor(dictionary=True)
        placeholders = ', '.join(['%s'] * len(categories))
        query = f"""
        SELECT a.*, s.summary, c.name as category
        FROM article a
        JOIN summaries s ON a.id = s.article_id
        JOIN categories c ON a.category_id = c.id
        WHERE c.name IN ({placeholders})
        ORDER BY a.created_at DESC
        LIMIT %s
        """
        try:
            cursor.execute(query, (*categories, limit))
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching articles for categories {categories}: {e}")
            return []
        finally:
            cursor.close()

    def article_exists(self, url):
        cursor = self.connection.cursor()
        query = "SELECT COUNT(*) FROM article WHERE link = %s"
        try:
            cursor.execute(query, (url,))
            count = cursor.fetchone()[0]
            return count > 0
        except Error as e:
            print(f"Error checking article existence: {e}")
            return False
        finally:
            cursor.close()

    def save_article(self, link, title, scrapy_text, source, category):
        cursor = self.connection.cursor()
        try:
            self.connection.start_transaction()

            # Zapisz lub pobierz kategorię
            cat_query = "INSERT IGNORE INTO categories (name) VALUES (%s)"
            cursor.execute(cat_query, (category,))

            cat_id_query = "SELECT id FROM categories WHERE name = %s"
            cursor.execute(cat_id_query, (category,))
            category_id = cursor.fetchone()[0]

            # Zapisz artykuł
            article_query = """
            INSERT INTO article (link, title, scrapy_text, source, category_id, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
            """
            cursor.execute(article_query, (link, title, scrapy_text, source, category_id))
            article_id = cursor.lastrowid

            self.connection.commit()
            return article_id

        except Error as e:
            self.logger.error(f"Error saving article: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def save_summary(self, article_id, summary_text, reader_type):
        cursor = self.connection.cursor()
        try:
            query = """
            INSERT INTO summaries (article_id, summary, reader_type, created_at)
            VALUES (%s, %s, %s, NOW())
            """
            cursor.execute(query, (article_id, summary_text, reader_type))
            self.connection.commit()
            return True
        except Error as e:
            self.logger.error(f"Error saving summary: {e}")
            return False
        finally:
            cursor.close()

    def get_article_summaries(self, article_id):
        cursor = self.connection.cursor(dictionary=True)
        try:
            query = """
            SELECT summary, reader_type, created_at
            FROM summaries
            WHERE article_id = %s
            ORDER BY created_at DESC
            """
            cursor.execute(query, (article_id,))
            return cursor.fetchall()
        except Error as e:
            self.logger.error(f"Error fetching summaries: {e}")
            return []
        finally:
            cursor.close()

    def generate_pdf_by_category(self, category):
        articles = self.get_articles_by_categories([category])
        if not articles:
            print(f"No articles found for category {category}")
            return None

        pdf_filename = os.path.join(os.getcwd(), f"{category}_newsletter.pdf")
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph(f"Newsletter: {category}", styles['Title']))
        story.append(Spacer(1, 12))

        for article in articles:
            story.append(Paragraph(article['title'], styles['Heading2']))
            story.append(Paragraph(article['summary'], styles['BodyText']))
            story.append(Paragraph(f"Link: {article['link']}", styles['BodyText']))
            story.append(Spacer(1, 12))

        doc.build(story)
        print(f"PDF generated: {pdf_filename}")
        return pdf_filename

    def search_articles(self, query):
        cursor = self.connection.cursor(dictionary=True)
        search_query = f"%{query}%"
        sql = """
        SELECT a.*, s.summary, c.name as category_name
        FROM article a
        LEFT JOIN summaries s ON a.id = s.article_id
        LEFT JOIN categories c ON a.category_id = c.id
        WHERE a.title LIKE %s OR a.scrapy_text LIKE %s
        """
        cursor.execute(sql, (search_query, search_query))
        results = cursor.fetchall()
        cursor.close()
        return results

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")
