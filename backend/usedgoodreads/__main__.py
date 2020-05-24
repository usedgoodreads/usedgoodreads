import time
import hashlib

from flask import jsonify

class KeyToIsbn(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String(), nullable=False, index=True)

    title = db.Column(db.String(), nullable=False)
    isbn = db.Column(db.String(), nullable=False)

    at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, key, title, isbn):
        self.key = key
        self.title = title
        self.isbn = isbn

    @staticmethod
    def get(key, ttl=timedelta(days=1)):
        valid = datetime.utcnow() - ttl

        return KeyToIsbn.query \
                .filter(KeyToIsbn.key == key) \
                .filter(KeyToIsbn.at >= valid) \
                .first()
from .base import app, db, q
from .models.book import Book
from .models.usedbook import UsedBook

def key_to_job_id(key):
    h = hashlib.blake2s()
    h.update(key.encode("utf-8"))
    return h.hexdigest()


class UsedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    isbn = db.Column(db.String(), nullable=False, index=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer, nullable=False)
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


def resolve_isbn(key):
    time.sleep(3)

    item = KeyToIsbn(key=key, title="Harry Potter, Book 2", isbn="9780393608328")

    db.session.add(item)
    db.session.commit()


def resolve_used_books(key):
    time.sleep(3)

    cache = KeyToIsbn.get(key=key)

    if not cache:
        return

    item = UsedBook(isbn=cache.isbn, title="Harry Potter 2",
            description="Book in good shape", price=5,
            link="http://example.com")

    db.session.add(item)
    db.session.commit()


# https://www.usedgoodreads.com/book/show/36236132-growing-a-revolution
@app.route("/book/show/<string:key>")
def book_show(key):
    cache = KeyToIsbn.get(key=key)

    if cache:
        books = UsedBook.get(isbn=cache.isbn)

        if books:
            results = [ { "title": v.title, "description": v.description } for v in books ]

            return jsonify({ "title": cache.title, "isbn": cache.isbn,
                             "results": results }), 200

    isbn_jid = key_to_job_id(f"resolve_isbn:{key}")
    isbn_job = q.fetch_job(isbn_jid)

    if isbn_job:
        return jsonify({ "status": "pending" }), 404

    used_books_jid = key_to_job_id(f"resolve_used_books:{key}")
    used_books_job = q.fetch_job(used_books_jid)

    if used_books_job:
        return jsonify({ "status": "pending" }), 404

    q.enqueue(resolve_isbn, key, job_timeout=60 * 1,
            ttl=60 * 60, job_id=isbn_jid)

    q.enqueue(resolve_used_books, key, job_timeout=60 * 1,
            ttl=60 * 60, job_id=used_books_jid, depends_on=isbn_jid)

    return jsonify({ "status": "enqueued" }), 404


def main():
    db.create_all()
    db.session.commit()

    # TODO: look into proper runners, e.g. guincorn
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
