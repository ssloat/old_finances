from finances import db

import datetime
import re

class InvTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acc  = db.Column(db.String)
    date = db.Column(db.Date)
    fund = db.Column(db.String)
    shares = db.Column(db.Float)
    action = db.Column(db.String)
    cost = db.Column(db.Float)
    price = db.Column(db.Float)

    def __init__(self, date, acc, fund, shares, cost, price, action):
        self.date   = date
        self.acc    = acc
        self.fund   = fund
        self.action = action
        self.cost   = cost
        self.shares = shares
        self.price  = price

    def __repr__(self):
        return "<InvTransaction(%s, %s, '%s' %f, %f, %f)>" % (
            self.date, self.fund, self.action, self.cost, self.shares, self.price
        )


class Portfolio(object):
    def __init__(self):
        self.entries = {}

    def add_401k(self):
        for row in db.session.query(InvTransaction):
            self.entries[row.fund] = self.entries.get(row.fund, [])
            self.entries[row.fund].append(row)

    def shares(self, fund, date):
        return sum([row.shares for row in self.entries.get(fund, []) if row.date <= date])

def parse_date(s):
    mm, dd, yyyy = map(int, s.split('/'))
    return datetime.date(yyyy, mm, dd)

def create_investments():
    for year in range(2006, 2016):
        with open('../files/401k_%s.csv' % year) as f:
            for line in f.read().splitlines():
                date, fund, action, cost, shares = line.split(',')
                date = parse_date(date)
                db.session.add( InvTransaction(date, '401k', fund, float(shares), float(cost), float(cost) / float(shares), action) )
        
    for yr in range(2012, 2016):
        with open('../files/brokerage_%s.csv' % yr, 'r') as f:
            for line in f.read().splitlines()[1:]:
                data = line[1:-1].split('","')
        
                if data[6] == 'SecurityTransactions':
                    if data[7] == 'Divd Reinv':
                        match = re.match(r'.* REINV AMOUNT +\$([0-9.]+) +REINV PRICE +\$([0-9.]+) +QUANTITY BOT +([0-9\.]+) .*', data[8])
                        cost, price, qty = [float(match.group(x)) for x in range(1, 4)] 
                        db.session.add( InvTransaction(parse_date(data[1]), 'Brokerage', data[9], qty, cost, price, data[7]) )

                    elif data[7] == 'Journal Entry':
                        match = re.match(r'.* \$(\d+\.\d+)', data[8])
        
                        db.session.add( InvTransaction(parse_date(data[1]), 'Brokerage', data[9], float(data[10]), float(data[-1]), float(match.group(1)), data[7]) )

                    elif data[7] == 'Stock Dividend':
                        match = re.match(r'.* ([0-9.]+) .*', data[8])

                        print parse_date(data[1]), 'Brokerage', data[9], data[10], 0.0, float(match.group(1)), data[7] 
                        db.session.add( InvTransaction(parse_date(data[1]), 'Brokerage', data[9], float(data[10]), 0.0, float(match.group(1)), data[7]) )

                    elif data[7] == 'Purchase ' or data[7] == 'Sale ':
                        match = re.match(r'.* FRAC SHR QUANTITY +(.\d+)', data[8])
                        asset, qty, price, cost = data[-4:]
                        qty = float(qty)
                        if match:
                            qty = qty + (1 if qty>0 else -1) * float(match.group(1))

                        cost = cost.replace(',', '') 
                        if cost[0] == '(':
                            cost = '-'+cost[1:-1]
                        db.session.add( InvTransaction(parse_date(data[1]), 'Brokerage', asset, qty, float(cost), float(price), data[7][:-1]) )

                    elif data[7] == 'DUDB':
                        pass
                    else:
                        raise Exception("Unknown Security Transaction: %s" % data)

                elif data[6] == 'DividendAndInterest':
                    if data[7] in ['Dividend', 'Lg Tm Cap Gain', 'Sh Tm Cap Gain']:
                        div = '-'+data[-1][1:-1] if data[-1][0] == '(' else data[-1]
                        db.session.add( InvTransaction(parse_date(data[1]), 'Brokerage', data[-4], 0.0, float(div), 0.0, data[7]) )
                    elif data[7] == 'Bank Interest':
                        pass
                    else:
                        raise Exception("Unknown type: %s %s" % (data[6], data[7]))

                elif data[6] == 'Other':
                    if data[7] == 'Reinvestment':
                        pass
                    elif data[7] == 'Journal Entry' and re.search(r'SLOAT CASH GRANT', data[8]):
                        pass
                        #Not Brokerage item
                        #db.session.add( BrokerageT(data[1], 'N/A', 0.0, float(div), 0.0, 'Cash Grant') )
                    else:
                        raise Exception("Unknown type: %s %s" % (data[6], data[7]))

                elif data[6] == 'FundTransfers':
                    if data[7] == 'Funds Transfer':
                        pass
                    else:
                        raise Exception("Unknown type: %s %s" % (data[6], data[7]))
                else:
                    raise Exception("Unknown category: %s %s" % (data[6], data[7]))


if __name__ == '__main__':
    from finances import app
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    app = app.test_client()
    db.create_all()

    create_investments()

    amounts = dict()
    for row in db.session.query(InvTransaction):
        amounts[row.fund] = amounts.get(row.fund, 0.0) + row.shares

    for k, v in amounts.items():
        print k, v

    #p = Portfolio()
    #p.add_401k()
    #f = 'VANG INST INDEX PLUS'
    #for d in [datetime.date(2015, 3, 31), datetime.date(2015, 4, 15), datetime.date(2015, 4, 30)]:
    #    print d, f, p.shares(f, d)

    #f = 'BAC'
    #for d in [datetime.date(2015, 3, 31), datetime.date(2015, 4, 15), datetime.date(2015, 4, 30)]:
    #    print d, f, p.shares(f, d)
