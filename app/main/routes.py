from flask import render_template, flash, redirect, url_for, request, current_app, send_file
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.forms import UpdatePreferencesForm
from app.models import Article, Category, Summary
from mining_summary.spiders.generatePDF import PDF

@bp.route('/')
@bp.route('/index')
def index():
    categories = Category.query.all()
    return render_template('home.html', title='Home', categories=categories)

@bp.route('/category/<string:category_name>')
def category(category_name):
    category = Category.query.filter_by(name=category_name).first_or_404()
    articles = Article.query.filter_by(category=category).order_by(Article.created_at.desc()).all()
    return render_template('category.html', title=category.name, category=category.name, articles=articles)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdatePreferencesForm()
    if form.validate_on_submit():
        current_user.update_preferences(form.preferences.data)
        db.session.commit()
        flash('Your preferences have been updated.', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.preferences.data = current_user.get_preferences()
    return render_template('user_profile.html', title='Profile', form=form)

@bp.route('/generate_newsletter')
@login_required
def generate_newsletter():
    pdf_generator = PDF()
    user_categories = current_user.get_preferences()
    pdf_path = pdf_generator.generate_pdf_by_category(user_categories[0])  # Generate for the first preferred category
    if pdf_path:
        return send_file(pdf_path, as_attachment=True)
    else:
        flash('Unable to generate newsletter PDF', 'error')
        return redirect(url_for('main.index'))

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    articles = Article.query.filter(Article.title.contains(query) | Article.scrapy_text.contains(query)).all()
    return render_template('search_results.html', title='Search Results', articles=articles, query=query)

@bp.route('/articles')
@login_required
def articles():
    articles = Article.query.order_by(Article.created_at.desc()).limit(20).all()
    return render_template('article.html', articles=articles, title='Latest Articles')

@bp.route('/article/<int:id>')
def article(id):
    article = Article.query.get_or_404(id)
    return render_template('article.html', article=article, title=article.title)

@bp.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    form = SubscriptionForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            user.preferences = json.dumps({'categories': form.preferences.data})
            user.subscribe()
        else:
            user = User(email=form.email.data, preferences=json.dumps({'categories': form.preferences.data}))
            user.set_password('temporary_password')  # Możesz zaimplementować system resetowania hasła
            user.subscribe()
            db.session.add(user)
        db.session.commit()
        flash('You have been subscribed to the newsletter!', 'success')
        return redirect(url_for('main.index'))
    return render_template('subscribe.html', form=form)

@bp.route('/unsubscribe')
@login_required
def unsubscribe():
    current_user.unsubscribe()
    db.session.commit()
    flash('You have been unsubscribed from the newsletter.', 'info')
    return redirect(url_for('main.profile'))

@bp.route('/latest_articles')
def latest_articles():
    articles = Article.query.order_by(Article.created_at.desc()).limit(10).all()
    return render_template('latest_articles.html', articles=articles)
@bp.route('/pdfs')
@login_required
def pdfs():
    categories = Category.query.all()
    return render_template('pdfs.html', categories=categories)

@bp.route('/generate_pdf/<category_name>')
@login_required
def generate_pdf(category_name):
    pdf_generator = PDF()
    pdf_path = pdf_generator.generate_pdf_by_category(category_name)
    if pdf_path:
        return send_file(pdf_path, as_attachment=True)
    else:
        flash('Unable to generate PDF for this category', 'error')
        return redirect(url_for('main.pdfs'))