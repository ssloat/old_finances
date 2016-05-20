from finances import db

import datetime
import monthdelta

class MortgageSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    principal = db.Column(db.Float)

    def __init__(self, date, principal):
        self.date = date
        self.principal = principal

    def __repr__(self):
       return "<MortgageSchedule('%s, %s')>" % (self.date, self.principal)

def create_mort_schedule():
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

#    md = MonthDelta(1)
    d = datetime.date(2012, 1, 1)
    for s in schs:
        db.session.add( MortgageSchedule(d, s) )
        d = d + monthdelta.MonthDelta(1)
    
