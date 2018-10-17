from flask import Blueprint, render_template, current_app, request
from blog.models import Book, BookCategory
book_bp = Blueprint('book', __name__)


@book_bp.route('/')
def index():
    return render_template('book/index.html')
