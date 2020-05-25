from datetime import datetime, timedelta
from ..base import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goodreads_key = db.Column(db.String(), nullable=False, index=True)
    title = db.Column(db.String(), nullable=False)
    isbn = db.Column(db.String(), nullable=False)
    at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, key, title, isbn):
        self.goodreads_key = key
        self.title = title
        self.isbn = isbn

    @staticmethod
    def get(key, ttl=timedelta(days=1)):
        valid = datetime.utcnow() - ttl

        return Book.query \
                   .filter(Book.goodreads_key == key) \
                   .filter(Book.at >= valid) \
                   .first()
