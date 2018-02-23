from pprint import pformat


class Exchange(object):
    """docstring for Exchange"""
    def __init__(self, base, term, code, name, depth=2):
        self.base   = base
        self.term   = term
        self.depth  = float(depth)

        self.book   = {}
        self.bid    = None
        self.ask    = None

        self.stamp  = None
        self.code   = code
        self.name   = name

        self.update()

    def symbol(self):
        return '{0}/{1}'.format(self.base, self.term)

    def update(self):
        return

    def __repr__(self):
        return """
{0}
You can buy @ {1} and sell @ {2} for a depth of {3} {4}""".format(
            pformat(self.book),
            self.ask,
            self.bid,
            self.depth,
            self.term
        )
