#!/usr/bin/env python

from book import Book
from pprint import pprint
import sys


def main(base, term, depth):
    book = Book(base, term, depth)

    pprint (book.bids)
    pprint (book.asks)
    print
    # book.bids[0][0] = .000101
    print 'arb opportunities'
    pprint (book.arbs())
    return
    # Check if arb exists between each exchange
    for i, e in enumerate(exchanges):
        print e
        # if i == len(exchanges): continue
        # for x in exchanges[i+1:]:



if __name__ == '__main__':
    depth = sys.argv[3] if len(sys.argv) > 3 else 2
    main(sys.argv[1], sys.argv[2], depth)