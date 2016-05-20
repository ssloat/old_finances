from finances import db

import datetime
import urllib
import re

class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    long_name = db.Column(db.String)

    prices = db.relationship("StockPrice") 

    def __init__(self, name, long_name=None):
        self.name = name
        self.long_name = long_name or name

    def __repr__(self):
       return "<Stock('%s, %s, %s')>" % (self.id or '', self.name, self.long_name)

class StockPrice(db.Model):
    __tablename__ = 'stock_prices'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'))
    opn = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.Float)
    adjclose = db.Column(db.Float)

    stock = db.relationship("Stock")

    def __init__(self, date, stock, opn, high, low, close, volume, adjclose):
        self.date = date
        self.stock = stock
        self.opn = opn
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.adjclose = adjclose

    def __repr__(self):
       return "<StockPrice('%s, %s, %s, %f')>" % (self.id or '', self.date,
               self.stock, self.close)


URL = 'http://ichart.yahoo.com/table.csv'
def load_prices(start, end):
    print start, end
    stocks = [
#            'PG', 'AAPL', 'BAC', 'AET', 'HD',
#            'TWCGX', 'VGTSX', 'VFINX',
#            'VGSIX', 'VIPSX', 'FMKIX', 'FNMIX', 'BMBSX', 'VWAHX', 'PPUDX', 'PRDSX', 'VEIPX', 'VEXAX',
#            'VIIIX', 'VEMPX', 'VIPIX', 'PTTRX', 
#            'VOO',
#        'AMZN', 
        #'VTENX', 'VTXVX', 'VTWNX', 'VTTVX', 'VTHRX', 'VTTHX', 'VFORX', 'VTIVX', 'VFIFX', 'VFFVX', 'VTTSX',
        'VIPSX', 'VBILX', 'VSIGX', 'VFITX', 'VBLTX', 'VLGSX', 'VUSTX', 'VFISX', 'VTAPX',
    ]
    # MFS, Stable capital, Int Crdt

    for stock in stocks:
        s = db.session.query(Stock).filter_by(name=stock).first()
        if not s:
            s = Stock(stock)
            db.session.add(s)

        for p in db.session.query(StockPrice).\
                filter(StockPrice.stock==s, StockPrice.date >= start, StockPrice.date <= end):

#            print "Delete: %s" % p
            db.session.delete(p)

        #args = '?s=%s&a=5&b=10&c=%d&d=11&e=31&f=%d' % (stock, yr, yr)
        args = [
            's=%s' % (stock),
            'a=%d' % (start.month-1), 'b=%d' % (start.day), 'c=%d' % (start.year),
            'd=%d' % (end.month-1), 'e=%d' % (end.day), 'f=%d' % (end.year),
        ]

        lines = urllib.urlopen('%s?%s' % (URL, '&'.join(args))).readlines()
        if [x for x in lines if re.search('404 Not Found', x)]:
            print "Not found: %s: %s - %s" % (stock, start, end)
            continue

        for line in lines:
            if line[:4] == 'Date': 
                continue

            data = line[:-1].split(',')
            date = datetime.date(*map(int, data[0].split('-')))
    
            sp = StockPrice(date, s, *map(float, data[1:]))
#            print "Add: %s" % sp
            db.session.add(sp)

