from datetime import datetime
from flask_login import UserMixin
from blog.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    about = db.Column(db.TEXT)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    posts = db.relationship('Post', back_populates='category')

    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.TEXT)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    comment = db.Column(db.TEXT)

    category_id = db.Column(db.Integer, db.ForeignKey('book_category.id'))
    category = db.relationship('BookCategory', back_populates='books')


class BookCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)

    books = db.relationship('Book', back_populates='book_category')

    def delete(self):
        default_category = BookCategory.query.get(1)
        books = self.books[:]
        for book in books:
            book.category = default_category
        db.session.delete(self)
        db.session.commit()


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    url = db.Column(db.String(200), unique=True)

    category_id = db.Column(db.Integer, db.ForeignKey('link_category.id'))
    category = db.relationship('LinkCategory', back_populates='links')


class LinkCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)

    books = db.relationship('Link', back_populates='link_category')

    def delete(self):
        default_category = LinkCategory.query.get(1)
        links = self.links[:]
        for link in links:
            link.category = default_category
        db.session.delete(self)
        db.session.commit()


