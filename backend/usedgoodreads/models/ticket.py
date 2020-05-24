import hashlib


class Ticket:

    def __init__(self, key):
        self.goodreads_key = key

    @property
    def isbn_jid(self):
        h = hashlib.blake2s()
        key = f"resolve_isbn:{self.goodreads_key}"
        h.update(key.encode("utf-8"))
        return h.hexdigest()

    @property
    def used_books_jid(self):
        h = hashlib.blake2s()
        key = f"resolve_used_books:{self.goodreads_key}"
        h.update(key.encode("utf-8"))
        return h.hexdigest()
