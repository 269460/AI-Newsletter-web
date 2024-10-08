from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(255), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    scrapy_text = db.Column(db.Text)
    source = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_new = db.Column(db.Boolean, default=True)
    views = db.Column(db.Integer, default=0)
    summary = db.relationship('Summary', backref='article', uselist=False)

class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    summary = db.Column(db.Text)
    category = db.Column(db.String(50))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    preferences = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)

    def get_preferences(self):
        return self.preferences.split(',') if self.preferences else []

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_preferences(self, new_preferences):
        self.preferences = ','.join(new_preferences)
        db.session.commit()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
