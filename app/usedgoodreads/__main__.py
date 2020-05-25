from .base import app, db, q
from flask import render_template

from usedgoodreads.models.book import Book
from usedgoodreads.models.usedbook import UsedBook
from usedgoodreads.models.ticket import Ticket

from usedgoodreads.jobs import resolve_goodreads_key
from usedgoodreads.jobs import resolve_used_books


# https://www.usedgoodreads.com/book/show/36236132-growing-a-revolution
@app.route("/book/show/<string:key>")
def index(key):
    cache = Book.get(key=key)

    if cache:
        books = UsedBook.get(isbn=cache.isbn)

        if books:
            results = [{"title": v.title, "description": v.description} for v in books]

            return render_template("index.html", isbn=cache.isbn, title=cache.title,
                                   results=results)

    ticket = Ticket(key)

    if q.fetch_job(ticket.isbn_jid):
        return render_template("index.html")

    if q.fetch_job(ticket.used_books_jid):
        return render_template("index.html")

    q.enqueue(resolve_goodreads_key, ticket, job_timeout=60 * 1,
            ttl=60 * 60, job_id=ticket.isbn_jid)

    q.enqueue(resolve_used_books, key, job_timeout=60 * 1,
              ttl=60 * 60, job_id=ticket.used_books_jid, depends_on=ticket.isbn_jid)

    return render_template("index.html")


def main():
    db.create_all()
    db.session.commit()

    # TODO: look into proper runners, e.g. guincorn
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
