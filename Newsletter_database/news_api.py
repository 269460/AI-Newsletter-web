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

    def save_article(self, link, title, scrapy_text, source, category_id):
        query = """INSERT INTO article (link, title, scrapy_text, source, category_id) 
                   VALUES (%s, %s, %s, %s, %s)"""
        values = (link, title, scrapy_text, source, category_id)
        try:
            cursor.execute(query, values)
            self.connection.commit()
            print(f"Article saved: {title}")
            return cursor.lastrowid
        except Error as e:
            print(f"Error saving article: {e}")
            return None
        finally:
            cursor.close()

    def save_summary(self, article_id, summary):
        query = """INSERT INTO summaries (article_id, summary) 
                   VALUES (%s, %s)"""
        values = (article_id, summary)
        try:
            cursor.execute(query, values)
            self.connection.commit()
            print(f"Summary saved for article ID: {article_id}")
        except Error as e:
            print(f"Error saving summary: {e}")
        finally:
            cursor.close()

    def get_categories(self):
        cursor = self.connection.cursor()
        query = "SELECT name FROM categories"
        try:
            cursor.execute(query)
            return [category[0] for category in cursor.fetchall()]
        except Error as e:
            print(f"Error fetching categories: {e}")
            return []
        finally:
            cursor.close()

    def add_subscription(self, user_id, category_name, frequency='weekly'):
        cursor = self.connection.cursor()
        query = """INSERT INTO subscriptions (user_id, category_id, frequency)
                   SELECT %s, id, %s FROM categories WHERE name = %s"""
        values = (user_id, frequency, category_name)
        try:
            cursor.execute(query, values)
            self.connection.commit()
            print(f"Subscription added for user {user_id} to category {category_name}")
        except Error as e:
            print(f"Error adding subscription: {e}")
        finally:
            cursor.close()

    def get_user(self, user_id):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE id = %s"
        try:
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error fetching user with id {user_id}: {e}")
            return None
        finally:
            cursor.close()

    def get_articles_by_categories(self, categories, limit=5):
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


    def get_all_users(self):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM users"
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching all users: {e}")
            return []
        finally:
            cursor.close()

    def get_article(self, article_id):
        cursor = self.connection.cursor(dictionary=True)
        query = """
        SELECT a.*, s.summary, c.name as category_name
        FROM article a
        LEFT JOIN summaries s ON a.id = s.article_id
        LEFT JOIN categories c ON a.category_id = c.id
        WHERE a.id = %s
        """
        try:
            cursor.execute(query, (article_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error fetching article with id {article_id}: {e}")
            return None
        finally:
            cursor.close()

    def save_user(self, email, password, preferences):
        query = """INSERT INTO users (email, password_hash, preferences) 
                   VALUES (%s, %s, %s)"""
        hashed_password = generate_password_hash(password)
        values = (email, hashed_password, json.dumps(preferences))
        try:
            cursor.execute(query, values)
            self.connection.commit()
            print(f"User saved: {email}")
        except Error as e:
            print(f"Error saving user: {e}")
        finally:
            cursor.close()

    def get_users_by_category(self, category):
        cursor = self.connection.cursor()
        query = "SELECT email FROM users WHERE JSON_CONTAINS(preferences, %s, '$.categories')"
        try:
            cursor.execute(query, (json.dumps(category),))
            return [user[0] for user in cursor.fetchall()]
        except Error as e:
            print(f"Error fetching users for category {category}: {e}")
            return []
        finally:
            cursor.close()

    def update_article(self, article_id, title=None, scrapy_text=None, source=None, category_id=None):
        cursor = self.connection.cursor()
        query = "UPDATE article SET "
        values = []
        if title:
            query += "title = %s, "
            values.append(title)
        if scrapy_text:
            query += "scrapy_text = %s, "
            values.append(scrapy_text)
        if source:
            query += "source = %s, "
            values.append(source)
        if category_id:
            query += "category_id = %s, "
            values.append(category_id)
        query = query.rstrip(', ') + " WHERE id = %s"
        values.append(article_id)

        try:
            cursor.execute(query, tuple(values))
            self.connection.commit()
            print(f"Article updated: ID {article_id}")
        except Error as e:
            print(f"Error updating article: {e}")
        finally:
            cursor.close()

    def remove_subscription(self, user_id, category_name):
        cursor = self.connection.cursor()
        query = """DELETE FROM subscriptions 
                   WHERE user_id = %s AND category_id = (SELECT id FROM categories WHERE name = %s)"""
        values = (user_id, category_name)
        try:
            cursor.execute(query, values)
            self.connection.commit()
            print(f"Subscription removed for user {user_id} from category {category_name}")
        except Error as e:
            print(f"Error removing subscription: {e}")
        finally:
            cursor.close()

    def update_user_preferences(self, user_id, new_preferences):
        cursor = self.connection.cursor()
        query = "UPDATE users SET preferences = %s WHERE id = %s"
        values = (json.dumps(new_preferences), user_id)
        try:
            cursor.execute(query, values)
            self.connection.commit()
            print(f"Preferences updated for user {user_id}")
        except Error as e:
            print(f"Error updating user preferences: {e}")
        finally:
            cursor.close()

    def article_exists(self, link):
        cursor = self.connection.cursor()
        query = "SELECT id FROM article WHERE link = %s"
        try:
            cursor.execute(query, (link,))
            result = cursor.fetchone()
            return result is not None
        except Error as e:
            print(f"Error checking if article exists: {e}")
            return False
        finally:
            cursor.close()

    def generate_pdf_by_category(self, category):
        articles = self.get_articles_by_category(category)
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

    def get_article_count(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM article")
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def get_new_article_count(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM article WHERE DATE(created_at) = CURDATE()")
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

