import datetime
from exchange import Exchange
from pprint import pformat
import requests


BITFINEX_URL = 'https://api.bitfinex.com/v2/book/'


class Bitfinex(Exchange):
    """docstring for Bitfinex"""
    def __init__(self, base, term, depth=2):
        super(Bitfinex, self).__init__(base, term, 'BFX', 'Bitfinex', depth)

    def symbol(self):
        return '{0}{1}'.format(self.base.upper(), self.term.upper())

    def update(self):
        symbol = self.symbol()

        # print 'Sending get request to {0}..'.format(self.__class__.__name__),
        resp = requests.get(BITFINEX_URL + 't{0}/P0'.format(symbol))
        # print 'Response received!'
        
        if not resp.ok:
            print 'Error in {0} request: {1}'.format(self.__class__.__name__, resp.status_code)
            return

        resp = resp.json()
        book = {
            'bids': [[px,  vol] for px, _, vol in resp if vol >  0],
            'asks': [[px, -vol] for px, _, vol in resp if vol <= 0],
        }

        for side, depth in book.items():
            base  = 0
            term  = 0
            last  = -1
            for i, (px, vol) in enumerate(book[side]):
                term += vol
                if base <= self.depth: last = i
                base += vol * px
                book[side][i].append(base)
                book[side][i].append(term)

            self.book[side] = book[side][:last + 1]

            price = book[side][last][-2] / book[side][last][-1]
            if side == 'bids': self.bid = price
            else:              self.ask = price

        self.stamp = datetime.datetime.utcnow()

