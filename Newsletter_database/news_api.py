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
            print(f"Error connecting to MySQL database: {e}")
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