import os
from os.path import join, dirname
from dotenv import load_dotenv
from goodreads import client

def main():
    grc = get_gr_client()
    bookid = 52668915

    book = grc.book(bookid)
    print("{} [ISBN {}]".format(book.title, book.isbn13))

def setup_environment():
    """Setup environment
    """
    dotenv_path = join(dirname(__file__), 'goodreads.env')
    load_dotenv(dotenv_path)

def get_gr_client(environment_ready = False):
    """Get GoodReads API client
    """
    if not environment_ready:
        setup_environment()
    gr_api_key = os.getenv('GOOD_READS_KEY')
    gr_api_secret = os.getenv('GOOD_READS_SECRET')
    return client.GoodreadsClient(gr_api_key, gr_api_secret)

if __name__ == '__main__':
    main()
