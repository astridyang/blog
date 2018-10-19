import os
import click

from flask import Flask, render_template
from flask_wtf.csrf import CSRFError

from blog.settings import config
from blog.blueprints.admin import admin_bp
from blog.blueprints.auth import auth_bp
from blog.blueprints.blog import blog_bp
from blog.blueprints.book import book_bp
from blog.blueprints.link import link_bp
from blog.extensions import db, login_manager, csrf, ckeditor, bootstrap, moment, migrate
from blog.models import Admin, Post, Category, Book, Link, BookCategory, LinkCategory


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('blog')
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)
    return app


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        book_categories = BookCategory.query.order_by(BookCategory.name).all()
        link_categories = LinkCategory.query.order_by(LinkCategory.name).all()
        return dict(admin=admin, categories=categories, book_categories=book_categories,
                    link_categories=link_categories)


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(link_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            db.drop_all()
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """Building Bluelog, just for you."""

        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username=username,
                name='Admin',
                blog_title='Free planets',
                blog_sub_title='頑張ってください。',
                about='anything'
            )
            admin.set_password(password)
            db.session.add(admin)
        db.session.commit()
        click.echo('Done.')

    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--book_category', default=10, help='Quantity of book categories, default is 10.')
    @click.option('--book', default=50, help='Quantity of books, default is 50.')
    @click.option('--link_category', default=10, help='Quantity of link categories, default is 10.')
    @click.option('--link', default=50, help='Quantity of links, default is 50.')
    def forge(category, post, book_category, book, link_category, link):
        """Generate fake data."""
        from blog.fakes import fake_categorise, fake_posts, fake_book_categorise, \
            fake_books, fake_link_categorise, fake_links

        db.drop_all()
        db.create_all()

        click.echo('Generating %d categories...' % category)
        fake_categorise(category)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating %d bookCategories...' % book_category)
        fake_book_categorise(book_category)

        click.echo('Generating %d books...' % book)
        fake_books(book)

        click.echo('Generating %d link_categories...' % link_category)
        fake_link_categorise(link_category)

        click.echo('Generating %d links...' % link)
        fake_links(link)

        click.echo('Done')


# todo
def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post, Category=Category,
                    Book=Book, BookCategory=BookCategory, Link=Link, LinkCategory=LinkCategory)
