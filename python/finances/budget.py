from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref

from finances import Base
from finances.category import Category
from finances.tax_rates import TaxDeduction
from finances.transaction import _mortgage

import datetime

class Budget(Base):
    __tablename__ = 'budgets'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    year = Column(Integer)
    status = Column(String)

    entries = relationship("BudgetEntry", 
                backref=backref('budget', remote_side=[id])
            )

    def __init__(self, name, year, status=None):
        self.name   = name
        self.year   = year
        self.status = 'Single'

    def __repr__(self):
       return "<Budget(%s, %d, %s)>" % (self.name, self.year, self.status)


class BudgetEntry(Base):
    __tablename__ = 'budget_entries'

    id         = Column(Integer, primary_key=True)
    name       = Column(String)
    monthy     = Column(Float)
    yearly     = Column(Float)

    budget_id   = Column(Integer, ForeignKey('budgets.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))

    category  = relationship("Category")

    def __init__(self, name, budget, category, monthly=None, yearly=None):
        self.name     = name
        self.budget   = budget
        self.category = category
        self.monthly  = monthly or 0.0
        self.yearly   = yearly  or 0.0

    def __repr__(self):
       return "<BudgetEntry(%s, %s, %s, %f, %f)>" % (
           self.name, self.budget, self.category, self.monthly, self.yearly
       )

    def amount(self):
        return 12*self.monthly + self.yearly

def create_budget(session):
    b = Budget('2015 Single, 3 roommates', 2015, 'Single')
    session.add(b)

    taxable    = session.query(Category).filter_by(name='taxable income').first()
    nontaxable = session.query(Category).filter_by(name='nontaxable income').first()
    pretax     = session.query(Category).filter_by(name='preTax').first()
    giving     = session.query(Category).filter_by(name='giving').first()
    mort_int   = session.query(Category).filter_by(name='mortgage int').first()
    mort_prin  = session.query(Category).filter_by(name='mortgage prin').first()
    prop_tax   = session.query(Category).filter_by(name='property tax').first()
    utils      = session.query(Category).filter_by(name='house utilities').first()
    ins        = session.query(Category).filter_by(name='house insurance').first()
        
    _401k = session.query(TaxDeduction).filter_by(name='401k', year=b.year).first()

    bofa = BudgetEntry('Bofa', b, taxable, 136000/12.0, 25000)
    session.add(bofa)

    session.add( 
        BudgetEntry('Bofa 401k match', b, nontaxable, 0.05*_401k.amount/12, 0.03*bofa.amount()) 
    )

    session.add( BudgetEntry('Rent', b, taxable, 12*(450+450+400)) )

    session.add( BudgetEntry('401k',             b, pretax, _401k.amount/12.0) )
    session.add( BudgetEntry('Health Insurance', b, pretax, 2.0*48.37) )
    session.add( BudgetEntry('Dental',           b, pretax, 2*9.67) )
    session.add( BudgetEntry('Vision',           b, pretax, 2*4.67) )
    session.add( BudgetEntry('Metra',            b, pretax, 130) )
    session.add( BudgetEntry('HSA',              b, pretax, 100) )

    session.add( BudgetEntry('John Stott', b, giving, 250) )
    session.add( BudgetEntry('Compassion', b, giving, 286) )
    session.add( BudgetEntry('GFA',        b, giving, 210) )
    session.add( BudgetEntry('Stars',      b, giving, 200) )
    session.add( BudgetEntry('Keane',      b, giving, 75) )
    session.add( BudgetEntry('Keith',      b, giving, 125) )
    session.add( BudgetEntry('Stanley',    b, giving, 100) )
    session.add( BudgetEntry('Rez',        b, giving, 2600, 5700) )


    session.add( BudgetEntry('House Insurance', b, ins, 800/12.0) )
    session.add( BudgetEntry('Property Tax',    b, prop_tax, 0, 10185) )

    payments = [_mortgage(session, datetime.date(b.year, m, 15)) for m in range(1, 13)]
    i = reduce(lambda x, y: x+y[0], payments, 0.0)
    p = reduce(lambda x, y: x+y[1], payments, 0.0)
    session.add( BudgetEntry('Interest', b, mort_int, i/12.0) )
    session.add( BudgetEntry('Principal', b, mort_prin, p/12.0) )

    session.add( BudgetEntry('Nicor',       b, utils, 125) )
    session.add( BudgetEntry('Water',       b, utils, 125) )
    session.add( BudgetEntry('ComEd',       b, utils, 125) )
    session.add( BudgetEntry('TV/Internet', b, utils, 125) )

    
