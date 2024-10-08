
from flask import render_template, abort
from flask_login import login_required, current_user
from app.admin import bp
from app.models import User, Article

@bp.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    user_count = User.query.count()
    article_count = Article.query.count()
    new_articles = Article.query.filter(Article.is_new == True).count()
    popular_articles = Article.query.order_by(Article.views.desc()).limit(5).all()
    return render_template('admin/dashboard.html', user_count=user_count,
                           article_count=article_count, new_articles=new_articles,
                           popular_articles=popular_articles)
