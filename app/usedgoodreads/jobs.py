import os
import urllib3
import time

from usedgoodreads.models.book import Book
from usedgoodreads.models.usedbook import UsedBook
from usedgoodreads.models.ticket import Ticket
from usedgoodreads.base import db

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

pool = urllib3.PoolManager()


# Some links are not working:
# localhost:5000/book/show/136251.Harry_Potter_and_the_Deathly_Hallows
def resolve_goodreads_key(ticket):
    assert(isinstance(ticket, Ticket))
    url = f"https://www.goodreads.com/book/show/{ticket.goodreads_key}"
    r = pool.request("GET", url)
    if r.status != 200:
        msg = f"Expected HTML response 200, got {r.status} by {r.geturl()}"
        raise Exception(msg)

    soup = BeautifulSoup(r.data, "html.parser")
    isbn = soup.find('meta', attrs=dict(property="books:isbn")).get('content')
    title = soup.find('meta', attrs=dict(property="og:title")).get('content')
    item = Book(ticket.goodreads_key, title, isbn)

    db.session.add(item)
    db.session.commit()


def resolve_used_books(key):
    book = Book.get(key)
    ebay_books = get_used_books_from_kleinanzeigen(book)

    for b in ebay_books:
        db.session.add(b)

    db.session.commit()


def get_used_books_from_kleinanzeigen(book):
    url = "https://www.ebay-kleinanzeigen.de/s-buecher-zeitschriften/c76"
    options = Options()
    options.headless = True
    options.set_capability("javascriptEnabled", True)

    SELENIUM_HOST = os.getenv("SELENIUM_HOST")
    SELENIUM_PORT = os.getenv("SELENIUM_PORT")
    command_executor = f"http://{SELENIUM_HOST}:{SELENIUM_PORT}/wd/hub"

    driver = webdriver.Remote(
        command_executor=command_executor,
        desired_capabilities=options.to_capabilities()
    )
    driver.get(url)  # books
    gdpr = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "gdpr-banner-accept")))
    gdpr.click()

    search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "site-search-query")))
    try:
        search.send_keys(book.title)
    except TypeError as e:
        raise TypeError(f"TE: {book.title} / {e}")
    search.send_keys(Keys.RETURN)

    time.sleep(5)
    results = driver.find_elements_by_id("srchrslt-adtable")

    if not results:
        return []

    result = results[0]
    assert result.tag_name == "ul"
    return [single_searchresult_to_bookoffer(item, book.isbn)
            for item in result.find_elements_by_class_name("lazyload-item")]


def get_used_books_from_rebuy(book):
    url = "https://www.rebuy.de/kaufen/suchen?q={}&c=91".format(escape(book.title.replace(" ", "%20")))
    raise NotImplementedError()


def get_used_books_from_booklooker(book):
    url = "https://www.booklooker.de/B%C3%BCcher/Angebote/isbn={}".format(book.isbn)
    raise NotImplementedError()


def get_used_books_from_amazon(book):
    url = "https://www.amazon.de/s?i=stripbooks&rh=p_66%3A{}".format(book.isbn)
    raise NotImplementedError()


def single_searchresult_to_bookoffer(item, isbn):
    main = item.find_element_by_class_name("aditem-main")
    a = main.find_element_by_tag_name("a")
    title = a.text
    link = a.get_attribute("href")
    desc = main.find_element_by_tag_name("p").text

    details = item.find_element_by_class_name("aditem-details")
    # date = item.find_element_by_class_name("aditem-addon").text
    price = details.find_element_by_tag_name("strong")
    price_int = price.text.split()
    price = 10**9  # TODO: :)

    # TODO fix price parsing
    for i in price_int:
        try:
            price = int(i)
        except ValueError:
            continue
        else:
            break

    return UsedBook(isbn=isbn, title=title, description=desc,
                    price=price, link=link)
