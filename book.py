from exchanges.bancor       import Bancor
from exchanges.bitfinex     import Bitfinex
from exchanges.bittrex      import Bittrex
from exchanges.huobi        import Huobi
from exchanges.tidex        import Tidex
from pprint import pprint


class Book(object):
    """docstring for Book"""
    def __init__(self, base, term, depth=2.):
        self.base = base
        self.term = term
        self.depth = depth

        self.bids = []
        self.asks = []

        self.populate()

    def populate(self):
        self.exchanges = [
            Bancor(self.base, self.term),
            Tidex(self.base, self.term, self.depth),
            Huobi(self.base, self.term, self.depth),
            Bittrex(self.base, self.term),
            Bitfinex(self.base, self.term, self.depth),
        ]

        for e in self.exchanges:
            if e.bid != None:
                self.bids.append([e.bid, e.depth, e.code, e.stamp])
            if e.ask != None:
                self.asks.append([e.ask, e.depth, e.code, e.stamp])

        self.bids = sorted(self.bids, reverse=True)
        self.asks = sorted(self.asks)

    def arbs(self):
        arbs = []
        for a in self.asks:
            l = len(arbs)
            for b in self.bids:
                if a[0] - b[0] < 0: arbs.append((a, b))
                else:               break

            if len(arbs) == l: break

        if arbs == []: return None

        return arbs

    # def add(self, ex):
    #     if any(ex.code in sub for sub in self.bids):
    #         self.update(ex)

    #     self.add_bid(ex)
    #     self.add_ask(ex)

    # def add_bid(self, bid):
    #     for price, depth, exchange, stamp in self.bids:
    #         pass

        