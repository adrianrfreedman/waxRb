import datetime
from exchange import Exchange
from pprint import pformat
import requests


BITTREX_URL = 'https://bittrex.com/api/v1.1/public/getmarketsummary?market='


class Bittrex(Exchange):
    """docstring for Bittrex"""
    def __init__(self, base, term, depth=2):
        super(Bittrex, self).__init__(base, term, 'BRX', 'Bittrex', depth)

    def symbol(self):
        return '{1}-{0}'.format(self.base.lower(), self.term.lower())

    def update(self):
        symbol = self.symbol()

        # print 'Sending get request to {0}..'.format(self.__class__.__name__),
        resp = requests.get(BITTREX_URL + symbol)
        # print 'Response received!'
        
        if not resp.ok:
            print 'Error in {0} request: {1}'.format(self.__class__.__name__, resp.status_code)
            return

        book = resp.json()

        if not book['success']:
            msg = book['message']
            print '{0} error:'.format(self.__class__.__name__),
            if msg == 'INVALID_MARKET':
                print '{0} not available'.format(symbol)
            else:
                print '{0}'.format(msg)
            return

        self.bid = book['result'][0]['Bid']
        self.ask = book['result'][0]['Ask']

        self.depth = book['result'][0]['BaseVolume']
        self.stamp = datetime.datetime.strptime(book['result'][0]['TimeStamp'], "%Y-%m-%dT%H:%M:%S.%f")


