from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.main.forms import UpdatePreferencesForm
from app.models import Article, Category
from app.main.utils import generate_newsletter_pdf

@bp.route('/')
@bp.route('/index')
def index():
    categories = Category.query.all()
    return render_template('main/index.html', title='Home', categories=categories)

@bp.route('/category/<string:category_name>')
def category(category_name):
    category = Category.query.filter_by(name=category_name).first_or_404()
    articles = Article.query.filter_by(category=category).order_by(Article.created_at.desc()).all()
    return render_template('main/category.html', title=category.name, category=category, articles=articles)

@bp.route('/article/<int:id>')
def article(id):
    article = Article.query.get_or_404(id)
    return render_template('main/article.html', title=article.title, article=article)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdatePreferencesForm()
    if form.validate_on_submit():
        current_user.update_preferences(form.preferences.data)
        flash('Your preferences have been updated.')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.preferences.data = current_user.get_preferences()
    return render_template('main/profile.html', title='Profile', form=form)

@bp.route('/generate_newsletter')
@login_required
def generate_newsletter():
    pdf = generate_newsletter_pdf(current_user)
    return current_app.response_class(pdf, mimetype='application/pdf')

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    articles = Article.query.filter(Article.title.contains(query) | Article.content.contains(query)).all()
    return render_template('main/search_results.html', title='Search Results', articles=articles, query=query)
