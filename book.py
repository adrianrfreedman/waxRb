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

        self.arbs = []

        self.populate()

    def symbol(self):
        return '{0}/{1}'.format(self.base.upper(), self.term.upper())

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
                self.bids.append([e.bid, e.depth, e.name, e.stamp])
            if e.ask != None:
                self.asks.append([e.ask, e.depth, e.name, e.stamp])

        self.bids = sorted(self.bids, reverse=True)
        self.asks = sorted(self.asks)

    def eval_arbs(self, min_arb_pct=0.001):
        self.arbs = []
        self.min_arb_pct = min_arb_pct

        # Compare asks to bids to check for arb opportunities
        for a in self.asks:
            l = len(self.arbs)
            for b in self.bids:
                arb_pct = (b[0] - a[0]) / a[0]
                if arb_pct >= self.min_arb_pct: 
                    self.arbs.append((a, b, arb_pct))
                # As bids and asks are sorted, no need to look further down the stack if there is no match
                else: break

            # See previous comment
            if len(self.arbs) == l: break

    def what_arbs(self):
        if self.arbs == None: return 'No arbs evaluated yet!'
        elif self.arbs == []: return 'No arbs available!'

        return [
            'Buy {0} @ {1} on {2} and sell @ {3} on {4} for a gross return of {5}% (Timestamps: {6} and {7})'.format(
                self.symbol(), ask, ask_ex, bid, bid_ex,
                100 * round(pct, 1), str(ask_ts), str(bid_ts)
            ) 
            for (ask, _, ask_ex, ask_ts), (bid, _, bid_ex, bid_ts), pct
            in self.arbs
        ]



    # def add(self, ex):
    #     if any(ex.code in sub for sub in self.bids):
    #         self.update(ex)

    #     self.add_bid(ex)
    #     self.add_ask(ex)

    # def add_bid(self, bid):
    #     for price, depth, exchange, stamp in self.bids:
    #         pass

        