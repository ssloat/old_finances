from finances import db
from finances.models.category import Category
from finances.models.mort_schedule import MortgageSchedule

import datetime

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

def _mortgage(session, tdate):
    prin = 297000
    for q in session.query(Transaction).join(Category).\
            filter(Category.name=='mortgage prin', 
                    Transaction.tdate > datetime.date(2013, 3, 1),
                    Transaction.tdate < tdate):

        prin = prin - (-1 * q.amount)

    interest = float("%.2f" % (0.035 / 12 * prin))
    return interest, 1333.66 - interest

def mortgage(session, tdate, amt, trans_file):
    mint  = session.query(Category).filter_by(name='mortgage int').first()
    mprin = session.query(Category).filter_by(name='mortgage prin').first()

    interest, prin = _mortgage(session, tdate)

    session.add( Transaction(tdate, 'Chase', mint, -1 * interest, trans_file) )
    session.add( Transaction(tdate, 'Chase', mprin, -1 * prin, trans_file) )

def bac_mortgage(session, date, amt, trans_file):
    mint  = session.query(Category).filter_by(name='mortgage int').first()
    mprin = session.query(Category).filter_by(name='mortgage prin').first()
    ms    = session.query(MortgageSchedule).filter_by(date=date.replace(day=1)).first()

    session.add( Transaction(date, 'BAC', mprin, -1 * ms.principal, trans_file) )
    session.add( Transaction(date, 'BAC', mint, amt + ms.principal, trans_file) )

AMTS = None

def bofa(session, tdate, amt, trans_file):
    cats = [ ('taxable income', 'Bofa'), ('preTax', '401k'),
            ('inc taxes', 'Fed Taxes'), ('inc taxes', 'IL Taxes'), 
            ('inc taxes', 'Soc Sec'), ('inc taxes', 'Medicaid'),
            ('preTax', 'medical'), ('preTax', 'dental'),
            ('preTax', 'vision'), ('preTax', 'hsa'),
            ('preTax', 'Metra'), ('car', 'Metra'),
        ]

    global AMTS
    if not AMTS:
        AMTS = {}
        with open('files/salary.txt') as f:
            for line in f.read().splitlines():
                if not line or line[0] == '#' or ':' not in line: continue
                line = line.replace(' ', '')
                line = line.replace('(', '')
                line = line.replace(')', '')
                k, v = line.split(':')

                AMTS[int(k)] = map(float, [x for x in v.split(',') if x])

    c = session.query(Category).filter_by(name="bofa chk").first()
    session.add( Transaction(tdate, "xfer to USAA", c, -25, trans_file) )
    vals = AMTS[int(amt)]
    yearly = True if amt > 10000.0 else False
    for i in range(len(vals)):
        c = session.query(Category).filter_by(name=cats[i][0]).first()
        if vals[i] == 0:
            continue
        session.add( Transaction(tdate, cats[i][1], c, vals[i], trans_file, yearly=yearly) )


