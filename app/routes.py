from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.forms import LoginForm, RegistrationForm, UpdatePreferencesForm
from app.models import User
from Newsletter_database.news_api import NewsAPI

news_api = NewsAPI()

@app.route('/')
@app.route('/home')
def home():
    categories = news_api.get_categories()
    return render_template('home.html', categories=categories)

@app.route('/category/<string:category>')
def category(category):
    articles = news_api.get_articles_by_category(category)
    return render_template('category.html', category=category, articles=articles)

@app.route('/article/<int:article_id>')
def article(article_id):
    article = news_api.get_article(article_id)
    return render_template('article.html', article=article)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdatePreferencesForm()
    if form.validate_on_submit():
        current_user.update_preferences(form.preferences.data)
        flash('Your preferences have been updated.')
        return redirect(url_for('profile'))
    return render_template('user_profile.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        user.preferences = ','.join(form.preferences.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    articles = news_api.search_articles(query)
    return render_template('search_results.html', articles=articles, query=query)

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    user_count = User.query.count()
    article_count = news_api.get_article_count()
    new_articles = news_api.get_new_article_count()
    popular_articles = news_api.get_popular_articles()
    return render_template('admin_dashboard.html', user_count=user_count,
                           article_count=article_count, new_articles=new_articles,
                           popular_articles=popular_articles)

@app.route('/generate_pdf/<string:category>')
@login_required
def generate_pdf(category):
    pdf_file = news_api.generate_pdf_by_category(category)
    return send_file(pdf_file, as_attachment=True, attachment_filename=f"{category}_newsletter.pdf")

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
