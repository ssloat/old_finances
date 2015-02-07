from sqlalchemy import Column, Integer, Float, Date

#from finances import Base, session, engine
from finances import Base

import datetime
from monthdelta import MonthDelta

class MortgageSchedule(Base):
    __tablename__ = 'mortgage_schedule'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    principal = Column(Float)

    def __init__(self, date, principal):
        self.date = date
        self.principal = principal

    def __repr__(self):
       return "<MortgageSchedule('%s, %s')>" % (self.date, self.principal)

def create_mort_schedule(session):
    schs = [
        414.40,
        415.91,
        417.43,
        418.95,
        420.48,
        422.01,
        423.55,
        425.09,
        426.64,
        428.2,
        429.76,
        431.33,
        432.90,
        434.48,
        436.06,
        437.65,
    ]

    md = MonthDelta(1)
    d = datetime.date(2012, 1, 1)
    for s in schs:
        session.add( MortgageSchedule(d, s) )
        d = d + md
    
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


