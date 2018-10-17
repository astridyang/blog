from flask import Blueprint, render_template, current_app, request
from blog.models import Link, LinkCategory
link_bp = Blueprint('link', __name__)


@link_bp.route('/')
def index():
    return render_template('link/index.html')
