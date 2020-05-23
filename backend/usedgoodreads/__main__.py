import os
import time
import hashlib
from datetime import datetime, timedelta

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from redis import Redis
from rq import Queue

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
q = Queue(connection=Redis(host=os.getenv("REDIS_HOST"),
                           port=os.getenv("REDIS_PORT")))


class KeyToIsbn(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String(), nullable=False, index=True)
    isbn = db.Column(db.String(), nullable=False)

    at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, key, isbn):
        self.key = key
        self.isbn = isbn

    @staticmethod
    def get(key, ttl=timedelta(days=1)):
        valid = datetime.utcnow() - ttl

        return KeyToIsbn.query \
                .filter(KeyToIsbn.key == key) \
                .filter(KeyToIsbn.at >= valid) \
                .first()


def key_to_isbn(key):
    v = KeyToIsbn.get(key=key)
    return v.isbn if v else None


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

    item = KeyToIsbn(key=key, isbn="9780393608328")

    db.session.add(item)
    db.session.commit()


def resolve_used_books(key):
    time.sleep(3)

    isbn = key_to_isbn(key)

    if not isbn:
        return

    item = UsedBook(isbn=isbn, title="Harry Potter",
            description="Book in good shape", price=5,
            link="http://example.com")

    db.session.add(item)
    db.session.commit()


# https://www.usedgoodreads.com/book/show/36236132-growing-a-revolution
@app.route("/book/show/<string:key>")
def book_show(key):
    isbn = key_to_isbn(key)

    if isbn:
        books = UsedBook.get(isbn)

        if books:
            return jsonify([ { "isbn": v.isbn, "title": v.title } for v in books]), 200

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
