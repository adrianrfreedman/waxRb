import datetime
from exchange import Exchange
from pprint import pprint, pformat
import requests


TOKENS = { 
    'ETH':      '5937d635231e97001f744267',
    'BNT':      '594bb7e468a95e00203b048d',
    'MANA':     '5a2cfacad0129700019a7270',
    'DRGN':     '5a3cb6868fb75500011ab51d',
    'OMG':      '5a086f93875e890001605abc',
    'ENJ':      '5a174c5145a97200011ad30a',
    'STORM':    '5a3800604b02a6ad9f85324f',
    'MNTP':     '5a03590f08849f0001097d29',
    'KIN':      '5a1d8d7b634e00000187855b',
    'STX':      '59d27d45acb3c12634d19efb',
    'GNO':      '59d745ff90509add31e9db14',
    'BMC':      '5a048e3078658d0001ffdab8',
    'WAX':      '5a37e92fed8a500001de70da',
    'IND':      '5a1af60e9f604e00011f09eb',
    'AIX':      '5a1327c9c92a1700011c7baf',
    'GNOBNT':   '59d74c1b90509a8807e9db0f',
    'WISH':     '5a17536c45a97200011ad30b',
    'ENJBNT':   '5a1ace8a967e9c6a2a5ac385',
    'INDBNT':   '5a1d75171b11f300016dc7a3',
    'BMCBNT':   '5a1d81011b11f300016dc7a4',
    'KINBNT':   '5a1d94593203d200012b8b74',
    'WISHBNT':  '5a1eca803203d200012b8b77',
    'OMGBNT':   '5a22a25d33a64900015489d2',
    'TAAS':     '5a2549266331db0001de1204',
    'TAASBNT':  '5a2552ba17c6e300015ca453',
    'STORMBNT': '5a2cf93be116dc0001fa9406',
    'MANABNT':  '5a2d030dd0129700019a72d5',
    'MNTPBNT':  '5a312b5b4c1019000197111e',
    'AIXBNT':   '5a36c11a9416220001faa380',
    'CAT':      '5a3794f26de5cb0001ce3993',
    'CATBNT':   '5a37989ced8a500001de23e9',
    'WAXBNT':   '5a37ebb3a88c2a00013bbd66',
    'DRGNBNT':  '5a3cb9eec4c2b60001f748a0',
    'WINGS':    '5a1ea498171b0100018277b0',
    'EOS':      '5a1eb21531b0890001c2b90a',
}
BANCOR_URL = 'https://api.bancor.network/0.1/currencies/{0}/ticker?fromCurrencyId={1}'


class Bancor(Exchange):
    """docstring for Bancor"""
    def __init__(self, base, term):
        super(Bancor, self).__init__(base, term, 'BNT', 'Bancor')

    def update(self):
        symbol = self.symbol()

        # print 'Sending get request to {0}..'.format(self.__class__.__name__),
        resp = requests.get(BANCOR_URL.format(TOKENS.get(self.base.upper()), TOKENS.get(self.term.upper())))
        # print 'Response received!'
        
        if not resp.ok:
            print 'Error in {0} request: {1}'.format(self.__class__.__name__, r.status_code)
            return

        book = resp.json()

        if 'errorCode' in book:
            error = book['errorCode']
            print '{0} error:'.format(self.__class__.__name__)
            if error == 'invalidObjectId':
                print '{0} not available'.format(symbol)
            else:
                print '{0}'.format(error)
            return

        self.bid    = book['data'][u'price']
        self.ask    = book['data'][u'price']
        self.depth  = float(book['data']['totalSupply']) * self.bid

        self.stamp  = datetime.datetime.utcnow()

    def __repr__(self):
        return """
You can buy @ {0} and sell @ {1} for a depth of {2} {3}""".format(
            self.ask,
            self.bid,
            self.depth,
            self.term
        )
