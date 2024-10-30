from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    current_app,
    send_file,
)
from flask_login import current_user, login_required

from Newsletter_database import news_api
from app import db
from app.main import bp
from app.forms import UpdatePreferencesForm, SubscriptionForm
from mining_summary.spiders.generatePDF import PDF
from app.models import Article, Category, Summary, User
import json


@bp.route("/")
@bp.route("/index")
def index():
    categories = Category.query.all()
    return render_template("home.html", title="Home", categories=categories)


@bp.route("/category/<string:category_name>")
def category(category_name):
    category = Category.query.filter_by(name=category_name).first_or_404()
    articles = (
        Article.query.filter_by(category=category)
        .order_by(Article.created_at.desc())
        .all()
    )
    return render_template(
        "category.html", title=category.name, category=category.name, articles=articles
    )


@bp.route("/generate_newsletter")
@login_required
def generate_newsletter():
    pdf_generator = PDF()
    user_categories = current_user.get_preferences()
    pdf_path = pdf_generator.generate_pdf_by_category(
        user_categories[0]
    )  # Generate for the first preferred category
    if pdf_path:
        return send_file(pdf_path, as_attachment=True)
    else:
        flash("Unable to generate newsletter PDF", "error")
        return redirect(url_for("main.index"))


@bp.route("/search")
def search():
    query = request.args.get("q", "")
    articles = Article.query.filter(
        Article.title.contains(query) | Article.scrapy_text.contains(query)
    ).all()
    return render_template(
        "search_results.html", title="Search Results", articles=articles, query=query
    )


@bp.route("/articles")
@login_required
def articles():
    articles = Article.query.order_by(Article.created_at.desc()).limit(20).all()
    return render_template("article.html", articles=articles, title="Latest Articles")


@bp.route("/article/<int:id>")
def article(id):
    article = Article.query.get_or_404(id)
    return render_template("article.html", article=article, title=article.title)


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdatePreferencesForm()
    if form.validate_on_submit():
        current_user.update_preferences(form.preferences.data)
        db.session.commit()
        flash("Your preferences have been updated.", "success")
        return redirect(url_for("main.profile"))
    elif request.method == "GET":
        form.preferences.data = current_user.get_preferences()
    is_subscribed = news_api.is_user_subscribed(current_user.id)
    return render_template(
        "user_profile.html", title="Profile", form=form, is_subscribed=is_subscribed
    )


from Newsletter_database.news_api import NewsAPI

news_api = NewsAPI()


@bp.route("/subscribe", methods=["GET", "POST"])
def subscribe():
    if current_user.is_authenticated:
        return redirect(url_for("main.profile"))
    form = SubscriptionForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if news_api.subscribe_user(user.id):
                flash("You have successfully subscribed to the newsletter.", "success")
            else:
                flash("There was an error subscribing to the newsletter.", "error")
        else:
            flash("Email not found. Please register first.", "error")
        return redirect(url_for("main.index"))
    return render_template("subscribe.html", title="Subscribe", form=form)


@bp.route("/unsubscribe")
@login_required
def unsubscribe():
    if news_api.unsubscribe_user(current_user.id):
        flash("You have been unsubscribed from the newsletter.", "info")
    else:
        flash("There was an error unsubscribing from the newsletter.", "error")
    return redirect(url_for("main.profile"))


@bp.route("/latest_articles")
def latest_articles():
    articles = Article.query.order_by(Article.created_at.desc()).limit(10).all()
    return render_template("latest_articles.html", articles=articles)


@bp.route("/pdfs")
@login_required
def pdfs():
    categories = Category.query.all()
    return render_template("pdfs.html", categories=categories)


@bp.route("/generate_pdf/<category_name>")
@login_required
def generate_pdf(category_name):
    pdf_generator = PDF()
    pdf_path = pdf_generator.generate_pdf_by_category(category_name)
    if pdf_path:
        return send_file(pdf_path, as_attachment=True)
    else:
        flash("Unable to generate PDF for this category", "error")
        return redirect(url_for("main.pdfs"))


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("errors/500.html"), 500
