import datetime
from exchange import Exchange
from pprint import pformat
import requests


TIDEX_URL = 'https://api.tidex.com/api/3/depth/'


class Tidex(Exchange):
    """docstring for Tidex"""
    def __init__(self, base, term, depth=2):
        super(Tidex, self).__init__(base, term, 'TDX', depth)

    def symbol(self):
        return '{0}_{1}'.format(self.base.lower(), self.term.lower())

    def update(self):
        symbol = self.symbol()

        # print 'Sending get request to {0}..'.format(self.__class__.__name__),
        resp = requests.get(TIDEX_URL + symbol)
        # print 'Response received!'
        
        if not resp.ok:
            # print 'Error in request', r.status_code
            return

        book = resp.json()

        if symbol not in book:
            # print 'Error:', book.get('error')
            return

        for b in ('bids', 'asks'):
            base  = 0
            term  = 0
            last  = -1
            for i, (px, vol) in enumerate(book[symbol][b]):
                term += vol
                if base <= self.depth: last = i
                base += vol * px
                book[symbol][b][i].append(base)
                book[symbol][b][i].append(term)

            self.book[b] = book[symbol][b][:last + 1]

            price = book[symbol][b][last][-2] / book[symbol][b][last][-1]
            if b == 'bids': self.bid = price
            else:           self.ask = price

        self.stamp  = datetime.datetime.utcnow()

