import os
import time
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

    key = db.Column(db.String(), nullable=False)
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


class UsedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    isbn = db.Column(db.String(), nullable=False)
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


def resolve_used_books(isbn):
    time.sleep(3)

    item = UsedBook(isbn=isbn, title="Harry Potter",
            description="Book in good shape", price=5,
            link="http://example.com")

    db.session.add(item)
    db.session.commit()


@app.route("/isbn/<string:key>")
def isbn(key):
    val = KeyToIsbn.get(key=key)

    if val:
        return jsonify({ "isbn": val.isbn }), 200
    else:
        # TODO: only enqueue if job not in-flight already; track in db
        q.enqueue(resolve_isbn, key)
        return jsonify({ "status": "pending" }), 404


@app.route("/book/<string:isbn>")
def book(isbn):
    vals = UsedBook.get(isbn)

    if vals:
        return jsonify([ { "isbn": v.isbn, "title": v.title } for v in vals]), 200
    else:
        # TODO: only enqueue if job not in-flight already; track in db
        q.enqueue(resolve_used_books, isbn)
        return jsonify({ "status": "pending" }), 404


def main():
    db.create_all()
    db.session.commit()

    # TODO: look into proper runners, e.g. guincorn
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
