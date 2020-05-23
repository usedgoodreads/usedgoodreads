import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from dataclasses import dataclass
from books import Book, BookOffer

def main():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    book = Book(title = "Herr der Ringe", ean = "978-3-86680-192-9")
    offers = EbayKleinanzeigen(book).get_offers(driver)
    print(offers)
    driver.close()

@dataclass
class EbayKleinanzeigen:
    book: Book

    @property
    def search_url(self):
        return "https://www.ebay-kleinanzeigen.de/s-buecher-zeitschriften/c76"

    def single_searchresult_to_bookoffer(self, item):
        main = item.find_element_by_class_name("aditem-main")
        a = main.find_element_by_tag_name("a")
        title = a.text
        link = a.get_attribute("href")
        desc = main.find_element_by_tag_name("p").text

        details = item.find_element_by_class_name("aditem-details")
        price = details.find_element_by_tag_name("strong").text
        date = item.find_element_by_class_name("aditem-addon").text
        return BookOffer(title=title, link=link, description=desc, price=price, creation_date=date)

    def get_offers(self, driver):
        driver.get(self.search_url)  # books
        gdpr = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "gdpr-banner-accept")))
        gdpr.click()

        search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "site-search-query")))
        search.send_keys(self.book.title)
        search.send_keys(Keys.RETURN)

        time.sleep(5)
        results = driver.find_elements_by_id("srchrslt-adtable")
        assert len(results) == 1
        result = results[0]
        assert result.tag_name == "ul"
        return [self.single_searchresult_to_bookoffer(item)
                for item in result.find_elements_by_class_name("lazyload-item")]

@dataclass
class Amazon:
    book: Book

    @property
    def search_url(self):
        return "https://www.amazon.de/s?i=stripbooks&rh=p_66%3A{}".format(self.book.ean)

    def single_searchresult_to_bookoffer(self, item):
        raise NotImplementedError

    def get_offers(self, driver):
        raise NotImplementedError

@dataclass
class Rebuy:
    book: Book

    @property
    def search_url(self):
        return "https://www.rebuy.de/kaufen/suchen?q={}&c=91".format(escape(book.title.replace(" ", "%20")))

    def single_searchresult_to_bookoffer(self, item):
        raise NotImplementedError

    def get_offers(self, driver):
        raise NotImplementedError

@dataclass
class Booklooker:
    book: Book

    @property
    def search_url(self):
        return  "https://www.booklooker.de/B%C3%BCcher/Angebote/isbn={}".format(book.ean)

    def single_searchresult_to_bookoffer(self, item):
        raise NotImplementedError

    def get_offers(self, driver):
        raise NotImplementedError

if __name__ == '__main__':
    main()
