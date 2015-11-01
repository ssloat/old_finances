from finances import db

from finances.models.stock import Stock, StockPrice
import monthdelta
import datetime

class InvTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account  = db.Column(db.String)
    date = db.Column(db.Date)
    fund = db.Column(db.String)
    shares = db.Column(db.Float)
    action = db.Column(db.String)
    cost = db.Column(db.Float)
    price = db.Column(db.Float)

    def __init__(self, date, account, fund, shares, cost, price, action):
        self.date    = date
        self.account = account
        self.fund    = fund
        self.action  = action
        self.cost    = cost
        self.shares  = shares
        self.price   = price

    def __repr__(self):
        return "<InvTransaction(%s, %s, '%s' %f, %f, %f)>" % (
            self.date, self.fund, self.action, self.cost, self.shares, self.price
        )


class Portfolio(object):
    def __init__(self):
        self.entries = {}

    def add_401k(self):
        for row in db.session.query(InvTransaction).order_by(InvTransaction.date):
            self.entries[row.account] = self.entries.get(row.account, {})
            self.entries[row.account][row.fund] = self.entries[row.account].get(row.fund, [])
            self.entries[row.account][row.fund].append(row)

    def shares(self, account, fund, date):
        return sum([row.shares for row in self.entries[account].get(fund, []) if row.date <= date])

    def value(self, account, fund, date):
        start = date + datetime.timedelta(days=-5)
        p = db.session.query(StockPrice).join(Stock).filter(
                Stock.name==fund, StockPrice.date>=start, StockPrice.date<=date
            ).order_by(db.desc(StockPrice.date)).first()
       
        if not p:
            print "No price: %s, %s, %s" % (account, fund, date)
            return

        shares = self.shares(account, fund, date)
        return [p.close, shares, p.close * shares]

    def historical_values(self, acc, fund, dates):
        return [self.value(acc, fund, d) or [0.0] for d in dates]

    def values(self, date):
        results = dict([(k, {}) for k in self.entries.keys()])
        for acc, v in self.entries.items():
            for fund in v.keys():
                if fund in ['Stable', 'MFS', 'IntCredit']:
                    continue

                results[acc][fund] = self.value(acc, fund, date)

        return results


def portfolio(start, end):
    dates = []
    while end > start:
        dates.append(end)

        end = end.replace(day=1)
        end = end - datetime.timedelta(days=1)

    p = Portfolio()
    p.add_401k()
    
    results = {'headings': [''] + [str(d) for d in dates], 'rows': [{'name': 'top'}]}

    for acc in ['BROKERAGE', '401k', 'ROTH']:
        acc_results = [] #{'name': acc, 'parent': 'top', 'values': [0.0 for d in dates]})

        for fund in sorted(p.entries[acc].keys()):
            data = [x[-1] for x in p.historical_values(acc, fund, dates)]
            if [x for x in data if x != 0.0]:
                acc_results.append({'name': fund, 'data': data, 'parent': acc.capitalize()})

        data = [sum(x) for x in zip(*[y['data'] for y in acc_results])]
        heading = {'name': acc.capitalize(), 'parent': 'top', 'data': data}
        results['rows'].extend([heading] + acc_results)

    return results

def fundprices(fund, start, end):
    prices = db.session.query(StockPrice).join(Stock).filter(
        Stock.name==fund, StockPrice.date>=start, StockPrice.date<=end
    ).order_by(db.desc(StockPrice.date))

    return [{'date': p.date, 'price': p.close} for p in prices]

  
