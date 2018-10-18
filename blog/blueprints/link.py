from flask import Blueprint, render_template, current_app, request
from blog.models import Link, LinkCategory
link_bp = Blueprint('link', __name__)


@link_bp.route('/link')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Link.query.order_by(Link.timestamp.desc()).paginate(page, per_page=per_page)
    links = pagination.items
    return render_template('link/index.html', links=links, pagination=pagination)


@link_bp.route('/link_category/<int:category_id>', methods=['GET', 'POST'])
def show_link_category(category_id):
    category = LinkCategory.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Link.query.with_parent(category).order_by(Link.timestamp.desc()).paginate(page, per_page=per_page)
    links = pagination.items
    return render_template('link/category.html', links=links, category=category, pagination=pagination)