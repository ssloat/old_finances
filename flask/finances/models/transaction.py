from finances import db
from finances.models.category import Category, allChildren
from finances.models.mort_schedule import MortgageSchedule

import datetime
import monthdelta

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tdate = db.Column(db.Date)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    file_id = db.Column(db.Integer, db.ForeignKey('trans_file.id'))
    name = db.Column(db.String)
    amount = db.Column(db.Float)
    bdate = db.Column(db.Date)
    yearly = db.Column(db.Boolean, default=False)

    category   = db.relationship("Category")
    trans_file = db.relationship("TransFile")

    def __init__(self, tdate, name, category, amount, trans_file, bdate=None, yearly=False):
        self.tdate      = tdate
        self.name       = name
        self.category   = category
        self.amount     = amount
        self.trans_file = trans_file
        self.bdate      = bdate or self.tdate
        self.yearly     = yearly

    def __repr__(self):
       return "<Tran('%d, %s, %s, %s, %s, %s, %s')>" % ((self.id or 0), self.tdate, self.name,
               self.category, self.amount, self.trans_file, self.bdate)

def _mortgage(tdate):
    prin = 297000
    for q in db.session.query(Transaction).join(Category).\
            filter(Category.name=='mortgage prin', 
                    Transaction.tdate > datetime.date(2013, 3, 1),
                    Transaction.tdate < tdate):

        prin = prin - (-1 * q.amount)

    interest = float("%.2f" % (0.035 / 12 * prin))
    return interest, 1333.66 - interest

def mortgage(tdate, amt, trans_file):
    mint  = db.session.query(Category).filter_by(name='mortgage int').first()
    mprin = db.session.query(Category).filter_by(name='mortgage prin').first()

    interest, prin = _mortgage(tdate)

    db.session.add( Transaction(tdate, 'Chase', mint, -1 * interest, trans_file) )
    db.session.add( Transaction(tdate, 'Chase', mprin, -1 * prin, trans_file) )

def bac_mortgage(date, amt, trans_file):
    mint  = db.session.query(Category).filter_by(name='mortgage int').first()
    mprin = db.session.query(Category).filter_by(name='mortgage prin').first()
    ms    = db.session.query(MortgageSchedule).filter_by(date=date.replace(day=1)).first()

    db.session.add( Transaction(date, 'BAC', mprin, -1 * ms.principal, trans_file) )
    db.session.add( Transaction(date, 'BAC', mint, amt + ms.principal, trans_file) )

AMTS = None

def bofa(tdate, amt, trans_file):
    cats = [ ('bofa income', 'Bofa'), ('preTax', '401k'),
            ('inc taxes', 'Fed Taxes'), ('inc taxes', 'IL Taxes'), 
            ('inc taxes', 'Soc Sec'), ('inc taxes', 'Medicaid'),
            ('preTax', 'medical'), ('preTax', 'dental'),
            ('preTax', 'vision'), ('preTax', 'hsa'),
            ('preTax', 'Metra'), ('monthly', 'Metra'),
        ]

    global AMTS
    if not AMTS:
        AMTS = {}
        with open('../files/salary.txt') as f:
            for line in f.read().splitlines():
                if not line or line[0] == '#' or ':' not in line: continue
                line = line.replace(' ', '')
                line = line.replace('(', '')
                line = line.replace(')', '')
                k, v = line.split(':')

                AMTS[int(k)] = map(float, [x for x in v.split(',') if x])

    c = db.session.query(Category).filter_by(name="bofa chk").first()
    db.session.add( Transaction(tdate, "xfer to USAA", c, -25, trans_file) )
    vals = AMTS[int(amt)]
    yearly = True if amt > 10000.0 else False
    for i in range(len(vals)):
        c = db.session.query(Category).filter_by(name=cats[i][0]).first()
        if vals[i] == 0:
            continue
        db.session.add( Transaction(tdate, cats[i][1], c, vals[i], trans_file, yearly=yearly) )


def monthly(from_date, to_date):
    from_date = from_date.replace(day=1)
    to_date = to_date.replace(day=1) + monthdelta.monthdelta(1)

    months = []
    tmpdate = datetime.date(from_date.year, from_date.month, from_date.day)
    while tmpdate < to_date:
        months.append(datetime.date(tmpdate.year, tmpdate.month, 1))
        tmpdate += monthdelta.monthdelta(1)

    cats = db.session.query(Category).all()
    catids = dict([(c.id, c.name) for c in cats])
    keys = [m.strftime('%Y-%m') for m in months]
    ts = db.session.query(Transaction)\
        .filter(Transaction.tdate>=from_date, Transaction.tdate<to_date, Transaction.yearly==False)

    cat_keys = {} 
    results = {}
    for t in ts:
        if t.category.id not in cat_keys:
            cat_keys[t.category.id] = [t.category.id]
            tmp = t.category.parent
            while tmp.name != 'top':
                cat_keys[t.category.id].append(tmp.id)
                tmp = tmp.parent

            cat_keys[t.category.id].append(tmp.id)

        for cid in cat_keys[t.category.id]:
            results[cid] = results.get(cid) or dict([(k, []) for k in keys])
            results[cid][t.tdate.strftime('%Y-%m')].append(t.amount) 

    table = {'headings': ['category', 'average'] + keys[::-1], 'rows': []}
    top = db.session.query(Category).filter(Category.name=='top').first()
    for cat in [top]+allChildren():
        cols = [(sum(results.get(cat.id, {k: []}).get(k, []), 0.0), k) for k in keys[::-1]]
        table['rows'].append({
            'category': cat,
            'data': cols, 
            'average': "%.2f" % (sum([c[0] for c in cols]) / len(cols)),
        })

    return table

