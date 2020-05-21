from grclient import get_gr_client
from flask import Flask, jsonify, redirect, escape

app = Flask(__name__)
GRC = get_gr_client()


# TODO all these need to be sanitized
# e.g. Harry Potter 7 does not work with ebay
# http://localhost:5000/api/v1/book/show/136251.Harry_Potter_and_the_Deathly_Hallows
def get_booklooker_search_url(book):
    return "https://www.booklooker.de/B%C3%BCcher/Angebote/isbn={}".format(book.isbn13)
def get_ebay_kleinanzeigen_search_url(book):
    return "https://www.ebay-kleinanzeigen.de/s-musik-film-buecher/{}/k0c73".format(escape(book.title.replace(" ", "-")))
def get_amazon_de_search_url(book):
    return "https://www.amazon.de/s?i=stripbooks&rh=p_66%3A{}".format(book.isbn13)
def get_rebuy_search_url(book):
    return "https://www.rebuy.de/kaufen/suchen?q={}&c=91".format(escape(book.title.replace(" ", "%20")))


@app.route('/api/v1/book/show/<int:goodreads_id><garbage>')
def book_information(goodreads_id, garbage):
    """API address to return minimal book information.
    """
    book = GRC.book(goodreads_id)

    booklooker_search_url = get_booklooker_search_url(book)
    ebay_kleinanzeigen_search_url = get_ebay_kleinanzeigen_search_url(book)
    amazon_de_search_url = get_amazon_de_search_url(book)
    rebuy_search_url = get_rebuy_search_url(book)

    json = dict(title=book.title,
                isbn=book.isbn13,
                rating=book.average_rating,
                booklooker_search_url=booklooker_search_url,
                ebay_kleinanzeigen_search_url=ebay_kleinanzeigen_search_url,
                amazon_de_search_url=amazon_de_search_url,
                rebuy_search_url=rebuy_search_url)
    return jsonify(json)

# TODO connect this to the API
@app.route('/book/show/<int:goodreads_id><garbage>')
def to_booklooker(goodreads_id, garbage):
    """Redirect to booklooker search.
    """
    book = GRC.book(goodreads_id)
    return redirect(get_booklooker_search_url(book))
