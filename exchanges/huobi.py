import datetime
from exchange import Exchange
from pprint import pformat
import requests


HUOBI_URL = 'https://api.huobi.pro/market/depth'


class Huobi(Exchange):
    """docstring for Huobi"""
    def __init__(self, base, term, depth=2):
        super(Huobi, self).__init__(base, term, 'HUO', 'Huobi', depth)

    def symbol(self):
        return '{0}{1}'.format(self.base.lower(), self.term.lower())

    def update(self):
        symbol = self.symbol()

        # print 'Sending get request to {0}..'.format(self.__class__.__name__),
        resp = requests.get(HUOBI_URL, params={'symbol': symbol, 'type': 'step0'})
        # print 'Response received!'
        
        if not resp.ok:
            print 'Error in request', resp.status_code
            print resp.json()
            print {'symbol': symbol, 'type': 'step0'}
            return

        book = resp.json()

        if 'tick' not in book:
            print 'Error:', book.get('error')
            return

        for b in ('bids', 'asks'):
            base  = 0
            term  = 0
            last  = -1
            for i, (px, vol) in enumerate(book['tick'][b]):
                term += vol
                if base <= self.depth: last = i
                base += vol * px
                book['tick'][b][i].append(base)
                book['tick'][b][i].append(term)

            self.book[b] = book['tick'][b][:last + 1]

            price = book['tick'][b][last][-2] / book['tick'][b][last][-1]
            if b == 'bids': self.bid = price
            else:           self.ask = price

        self.stamp  = datetime.datetime.utcfromtimestamp(book['ts'] / 1000.)

