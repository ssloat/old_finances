from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref

#from finances import Base, session, engine
from finances import Base
from finances.category import Category, CategoryRE
from finances.mort_schedule import MortgageSchedule
from finances.trans_file import TransFile

import re
import datetime

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    tdate = Column(Date)
    category_id = Column(Integer, ForeignKey('categories.id'))
    file_id = Column(Integer, ForeignKey('files.id'))
    name = Column(String)
    amount = Column(Float)
    bdate = Column(Date)
    yearly = Column(Boolean, default=False)

    category   = relationship("Category")
    trans_file = relationship("TransFile")

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


if __name__ == '__main__':

    '''
    bills = session.query(Category).filter_by(name='bills').first()

    comed1 = Transaction(datetime.date(2012, 10, 2), 'ComEd', bills, 150.2)
    comed2 = Transaction(datetime.date(2012, 9, 2), 'ComEd', bills, 130.2)
    comed3 = Transaction(datetime.date(2012, 11, 2), 'ComEd', bills, 180.2)

    session.add_all([comed1, comed2, comed3])

    for x in session.query(Transaction).filter_by(name='ComEd').all():
        print x

    '''
#    readTrans('../Downloads/August2012_7377.csv')
#    readTrans('../Downloads/September2012_7377.csv')
#    readTrans('../Downloads/October2012_7377.csv')
    readChkTrans('../Downloads/test_checking.csv')


