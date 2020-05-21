from grclient import get_gr_client
from flask import Flask, jsonify, redirect, escape

app = Flask(__name__)
GRC = get_gr_client()

# TODO connect this to the API
@app.route('/book/show/<int:goodreads_id><garbage>')
def to_booklooker(goodreads_id, garbage):
    """Redirect to booklooker search.
    """
    book = GRC.book(goodreads_id)
    booklooker_search_url = "https://www.booklooker.de/B%C3%BCcher/Angebote/isbn={}".format(book.isbn13)
    return redirect(booklooker_search_url)
