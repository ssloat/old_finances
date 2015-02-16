from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref

from finances import Base
from finances.category import Category

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

if __name__ == 'main':
    b = Budget('2015 Single', 2015, 'Single')

    top        = Category('top', None, 0)
    income     = Category('income', top)
    taxable    = Category('taxable income', income)
    nontaxable = Category('nontaxable income', income)

    bofa = BudgetEntry('Bofa', b, taxable, 136000/12.0, 25000)
    BudgetEntry('Bofa 401k match', b, nontaxable, 0.05*18000/12, 0.03*bofa.amount())

    BudgetEntry('Rent', b, taxable, 12*(450+450+400))

    pretax = Category('pretax', top)
    BudgetEntry('401k', b, pretax, 18000/12.0)
    BudgetEntry('Health Insurance', b, pretax, 2.0*48.37)
    BudgetEntry('Dental', b, pretax, 2*9.67)
    BudgetEntry('Vision', b, pretax, 2*4.67)
    BudgetEntry('Metra', b, pretax, 130)
    BudgetEntry('HSA', b, pretax, 100)

    giving = Category('giving', top)
    BudgetEntry('John Stott', b, giving, 250)
    BudgetEntry('Compassion', b, giving, 286)
    BudgetEntry('GFA',        b, giving, 210)
    BudgetEntry('Stars',      b, giving, 200)
    BudgetEntry('Keane',      b, giving, 75)
    BudgetEntry('Keith',      b, giving, 125)
    BudgetEntry('Stanley',    b, giving, 100)
    BudgetEntry('Rez',        b, giving, 2600, 5700)

    house = Category('house', top)
    BudgetEntry('House Insurance', b, house, 800/12.0)
    BudgetEntry('Principal', b, house, 5868/12.0)
    BudgetEntry('Interest', b, house, 10135/12.0)
    BudgetEntry('Property Tax', b, house, 0, 10185)

    utilities = Category('utilities', top)
    BudgetEntry('Nicor', b, utilities, 125)
    BudgetEntry('Water', b, utilities, 125)
    BudgetEntry('ComEd', b, utilities, 125)
    BudgetEntry('TV/Internet', b, utilities, 125)

    
