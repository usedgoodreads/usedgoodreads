import sys
from .base import app, db, q
from flask import render_template, abort

from usedgoodreads.models.book import Book
from usedgoodreads.models.usedbook import UsedBook
from usedgoodreads.models.ticket import Ticket

from usedgoodreads.jobs import resolve_goodreads_key
from usedgoodreads.jobs import resolve_used_books


# https://www.usedgoodreads.com/book/show/36236132-growing-a-revolution
@app.route("/book/show/<string:key>")
def index(key):
    cache = Book.get(key=key)
    ticket = Ticket(key)

    isbn = None
    title = None
    refresh = False
    status = None
    results = []

    if cache:
        # Book is in database
        books = UsedBook.get(isbn=cache.isbn)
        isbn = cache.isbn
        title = cache.title
        if books:
            # Used books are in database
            results = [{"title": v.title, "description": v.description,
                        "price": v.price, "link": v.link} for v in books]
            results.sort(key=lambda each: each["price"])
            refresh = False
        else:
            # Used books need to be fetched
            job = q.fetch_job(ticket.used_books_jid)
            refresh = False
            status = "Used books: pending"
            if job and job.get_status() == "finished":
                # job already fetched w/o results
                status = "Used books: No results"
                refresh = False
            elif job:
                # job still running or there was an error
                status = f"Used books: {job.get_status()}"
                refresh = True
            else:
                # Add fetch job to q
                q.enqueue(resolve_used_books, key, job_timeout=60 * 1,
                          ttl=60 * 60, job_id=ticket.used_books_jid)
                status = "Used books: enqueued"
                refresh = True
    else:
        # Book is not in database
        job = q.fetch_job(ticket.isbn_jid)
        status = "URL: pending"
        refresh = False
        if job:
            # Resolve task is already in q
            status = f"URL: {job.get_status()}"
            refresh = True
        else:
            # Add resolve task to q
            q.enqueue(resolve_goodreads_key, ticket, job_timeout=60 * 1,
                      ttl=60 * 60, job_id=ticket.isbn_jid)
            status = "URL: enqueued"
            refresh = True
    return render_template("index.html", isbn=isbn, title=title, results=results, status=status, refresh=refresh)


def main():
    db.create_all()
    db.session.commit()

    # TODO: look into proper runners, e.g. guincorn
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
