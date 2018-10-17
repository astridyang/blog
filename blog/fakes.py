import random

from faker import Faker
from sqlalchemy.exc import IntegrityError
from blog import db
from blog.models import Admin, Post, Category, Book, BookCategory, Link, LinkCategory

fake = Faker()


def fake_categorise(count=10):
    category = Category(name='default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )

        db.session.add(post)
    db.session.commit()


def fake_book_categorise(count=10):
    category = BookCategory(name='default')
    db.session.add(category)

    for i in range(count):
        category = BookCategory(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_books(count=50):
    for i in range(count):
        book = Book(
            name=fake.sentence(),
            comment=fake.text(2000),
            category=BookCategory.query.get(random.randint(1, BookCategory.query.count())),
            timestamp=fake.date_time_this_year()
        )

        db.session.add(book)
    db.session.commit()


def fake_link_categorise(count=10):
    category = LinkCategory(name='default')
    db.session.add(category)

    for i in range(count):
        category = LinkCategory(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_links(count=50):
    for i in range(count):
        link = Link(
            name=fake.sentence(),
            url=fake.url(),
            category=LinkCategory.query.get(random.randint(1, LinkCategory.query.count()))
        )

        db.session.add(link)
    db.session.commit()


