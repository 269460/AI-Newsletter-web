from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    preferences = db.Column(db.JSON)
    is_subscribed = db.Column(db.Boolean, default=False)

    def subscribe(self):
        self.is_subscribed = True

    def unsubscribe(self):
        self.is_subscribed = False

    def get_preferences(self):
        return self.preferences if self.preferences else []

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_preferences(self, new_preferences):
        self.preferences = new_preferences

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(255), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    scrapy_text = db.Column(db.Text)
    source = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('articles', lazy=True))
    summary = db.relationship('Summary', backref='article', uselist=False)

class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    summary = db.Column(db.Text)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    frequency = db.Column(db.Enum('daily', 'weekly', 'monthly'), default='weekly')
    user = db.relationship('User', backref=db.backref('subscriptions', lazy=True))
    category = db.relationship('Category', backref=db.backref('subscriptions', lazy=True))

    __table_args__ = (db.UniqueConstraint('user_id', 'category_id', name='_user_category_uc'),)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
