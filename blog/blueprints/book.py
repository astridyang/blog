from flask import Blueprint, render_template, current_app, request
from blog.models import Book, BookCategory
book_bp = Blueprint('book', __name__)


@book_bp.route('/book')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Book.query.order_by(Book.timestamp.desc()).paginate(page, per_page=per_page)
    books = pagination.items
    return render_template('book/index.html', books=books, pagination=pagination)


@book_bp.route('/book/<int:book_id>', methods=['GET', 'POST'])
def show_book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book/book.html', book=book)


@book_bp.route('/book_category/<int:category_id>', methods=['GET', 'POST'])
def show_book_category(category_id):
    category = BookCategory.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Book.query.with_parent(category).order_by(Book.timestamp.desc()).paginate(page, per_page=per_page)
    books = pagination.items
    return render_template('book/category.html', books=books, category=category, pagination=pagination)


