from dataclasses import dataclass
import re

def main():
    testing = [
        "0-596-52068-9",      # valid ISBN10
        "3930-3-3930-32",     # invalid
        "3744519465",         # valid ISBN10
        "978-0-596-52068-7",  # valid ISBN13
        "9783744500524",      # valid ISBN13
        "9780596520687",      # valid ISBN13
        "978-3-86680-192-9",  # valid ISBN13
    ]
    for k in testing:
        try:
            b = Book(title = "Fancy title", ean = k)
            print(b, b.isbn13, b.ean, b.isbn10)
        except:
            print(k, " not valid")

@dataclass
class Book:
    """ Book dataclass with EAN (European Article Number) and title of the book.

    Book dataclass represented by EAN (European Article Number). The EAN number
    as been chosen since it contains all possible book identifiers and many
    more. Further, the ISBN13 and ISBN10 identifiers can be calculated from the
    EAN.
    """
    title: str
    ean: int

    @property
    def ean(self):
        return self._ean

    @ean.setter
    def ean(self, value):
        """Check if string is a valid isbn expression

        Source
        ====
        https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch04s13.html
        """
        value = str(value)
        # Checks for ISBN-10 or ISBN-13 format
        regex = re.compile("^(?:ISBN(?:-1[03])?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$")
        is_isbn13 = False
        is_valid = False

        if regex.search(value):
            # Remove non ISBN digits, then split into a list
            chars = list(re.sub("[- ]|^ISBN(?:-1[03])?:?", "", value))
            # Remove the final ISBN digit from `chars`, and assign it to `last`
            last = chars.pop()
            is_isbn13 = False

            if len(chars) == 9:
                # Compute the ISBN-10 check digit
                check = self._compute_isbn10_checksum(chars)
            else:
                # Compute the ISBN-13 check digit
                is_isbn13 = True
                check = self._compute_isbn13_checksum(chars)
            if (str(check) == last):
                # valid ISBN number
                if is_isbn13:
                    chars += [str(check)]
                    self._ean = int("".join(chars))
                else:
                    chars = ["9","7","8"] + chars
                    check = self._compute_isbn13_checksum(chars)
                    chars += [str(check)]
                    self._ean = int("".join(chars))
            else:
                raise ValueError("Invalid check number for ISBN")  # Invalid check number
        else:
            raise TypeError("No valid ISBN number")  # simply no valid

    @staticmethod
    def _compute_isbn13_checksum(chars):
        val = sum((x % 2 * 2 + 1) * int(y) for x,y in enumerate(chars))
        check = 10 - (val % 10)
        if check == 10:
            check = "0"
        return check

    @staticmethod
    def _compute_isbn10_checksum(chars):
        val = sum((x + 2) * int(y) for x,y in enumerate(reversed(chars)))
        check = 11 - (val % 11)
        if check == 10:
            check = "X"
        elif check == 11:
            check = "0"
        return check

    @property
    def isbn13(self):
        check   = (self.ean % 10**1)
        title   = (self.ean % 10**4) - check
        group   = (self.ean % 10**9) - check - title
        country = (self.ean % 10**10) - check - title - group
        prefix  = self.ean - check - title - group - country
        return "{}-{}-{}-{}-{}".format(
            prefix // 10**10, country // 10**9, group // 10**4, title // 10**1, check
        )

    @property
    def isbn10(self):
        result = str(self.ean)
        chars = list(str(self.ean))[3:-1]
        check = self._compute_isbn10_checksum(chars)
        return "{}-{}-{}-{}".format(chars[0],"".join(chars[1:4]), "".join(chars[4:9]), check)


@dataclass
class BookOffer:
    title: str
    link: str
    description: str
    price: str
    creation_date: str


if __name__ == '__main__':
    main()
