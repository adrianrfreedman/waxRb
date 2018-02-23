#!/usr/bin/env python

from book import Book
from emails import arb_signals
from pprint import pprint
import sys


def main(base, term, depth):
    book = Book(base, term, depth)

    book.eval_arbs()
    if book.arbs:
        pprint(book.what_arbs());return
        arb_signals.email(book.what_arbs())



if __name__ == '__main__':
    depth = sys.argv[3] if len(sys.argv) > 3 else 2
    main(sys.argv[1], sys.argv[2], depth)