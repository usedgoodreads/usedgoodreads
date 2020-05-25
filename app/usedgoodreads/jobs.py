import urllib3
from bs4 import BeautifulSoup
from .base import db

from .models.book import Book
from .models.ticket import Ticket

pool = urllib3.PoolManager()

# Is not work for localhost:5000/book/show/136251.Harry_Potter_and_the_Deathly_Hallows
def resolve_goodreads_key(ticket):
    assert(isinstance(ticket, Ticket))
    url = f"https://www.goodreads.com/book/show/{ticket.goodreads_key}"
    r = pool.request("GET", url)
    if r.status != 200:
        raise Exception(f"Expected HTML response 200, got {r.status} by {r.geturl()}")

    soup = BeautifulSoup(r.data, "html.parser")
    isbn = soup.find('meta', attrs=dict(property="books:isbn")).get('content')
    title = soup.find('meta', attrs=dict(property="og:title")).get('content')
    item = Book(ticket.goodreads_key, title, isbn)

    db.session.add(item)
    db.session.commit()


def resolve_used_books_from_kleinanzeigen(book):
    raise NotImplementedError()


def resolve_used_books_from_rebuy(book):
    raise NotImplementedError()


def resolve_used_books_from_amazon(book):
    raise NotImplementedError()


def resolve_used_books_from_amazon(book):
    raise NotImplementedError()
