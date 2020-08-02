from datetime import datetime, timedelta
from usedgoodreads.base import db


class UsedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    isbn = db.Column(db.String(), nullable=False, index=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    price = db.Column(db.Float, nullable=False)
    link = db.Column(db.String(), nullable=False)

    at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, isbn, title, description, price, link):
        self.isbn = isbn
        self.title = title
        self.description = description
        self.price = price
        self.link = link

    @staticmethod
    def get(isbn, ttl=timedelta(days=1)):
        valid = datetime.utcnow() - ttl

        return UsedBook.query \
                       .filter(UsedBook.isbn == isbn) \
                       .filter(UsedBook.at >= valid) \
                       .all()

    def __hash__(self):
        return NotImplementedError()
