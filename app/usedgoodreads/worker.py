import time

from usedgoodreads.base import db
from usedgoodreads.models.book import Book
from usedgoodreads.models.usedbook import UsedBook


def resolve_isbn(key):
    time.sleep(3)

    item = Book(key=key, title="Harry Potter, Book 2", isbn="9780393608328")

    db.session.add(item)
    db.session.commit()


def resolve_used_books(key):
    time.sleep(3)

    cache = Book.get(key=key)

    if not cache:
        return

    item = UsedBook(isbn=cache.isbn, title="Harry Potter 2",
                    description="Book in good shape", price=5,
                    link="http://example.com")

    db.session.add(item)
    db.session.commit()
