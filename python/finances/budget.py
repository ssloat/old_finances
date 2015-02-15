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

    id     = Column(Integer, primary_key=True)
    name   = Column(String)
    monthy = Column(Float)
    yearly = Column(Float)

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

