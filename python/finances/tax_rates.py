from sqlalchemy import Column, Integer, String, Float

from finances import Base

class TaxDeduction(Base):
    __tablename__ = 'tax_deductions'

    id       = Column(Integer, primary_key=True)
    name     = Column(String)
    year     = Column(Integer)
    value    = Column(Integer)
    status   = Column(String)

    def __init__(self, name, year, amount, status=None):
        self.name   = name
        self.year   = year
        self.amount = amount
        self.status = status or 'Single'

    def __repr__(self):
       return "<TaxDeduction('%s', %d, %d, '%s')>" % (
           self.name, self.year, self.amount, self.status
       )

class TaxRate(Base):
    __tablename__ = 'tax_rates'

    id     = Column(Integer, primary_key=True)
    name   = Column(String)
    year   = Column(Integer)
    start  = Column(Integer)
    end    = Column(Integer)
    rate   = Column(Float)
    status = Column(String)

    def __init__(self, name, year, start, end, rate, status=None):
        self.name   = name
        self.year   = year
        self.start  = start
        self.end    = end
        self.rate   = rate
        self.status = status or 'Single'

    def __repr__(self):
       return "<TaxRate(%s %s %d: %d - %d => %f)>" % (
           self.name, self.status, self.year, self.start, self.end, self.rate,
       )


def add_tax_rates(session):
    session.add( TaxDeduction('Fed Standard', 2013, 6100, 'Single') )
    session.add( TaxDeduction('Fed Standard', 2014, 6200, 'Single') )

    session.add( TaxDeduction('Fed Standard', 2013, 8950, 'Head') )
    session.add( TaxDeduction('Fed Standard', 2014, 9100, 'Head') )

    session.add( TaxDeduction('Fed Standard', 2013, 12200, 'Joint') )
    session.add( TaxDeduction('Fed Standard', 2014, 12400, 'Joint') )

    session.add( TaxDeduction('Fed Standard', 2013, 6100, 'Separate') )
    session.add( TaxDeduction('Fed Standard', 2014, 6200, 'Separate') )

    session.add( TaxDeduction('401k', 2013, 17500) )
    session.add( TaxDeduction('401k', 2014, 18000) )

    session.add( TaxRate('Federal', 2014, 0,      9075,   .10,  'Single') )
    session.add( TaxRate('Federal', 2014, 9075,   36900,  .15,  'Single') )
    session.add( TaxRate('Federal', 2014, 36900,  89350,  .25,  'Single') )
    session.add( TaxRate('Federal', 2014, 89350,  186350, .28,  'Single') )
    session.add( TaxRate('Federal', 2014, 186350, 405100, .33,  'Single') )
    session.add( TaxRate('Federal', 2014, 405100, 406750, .35,  'Single') )
    session.add( TaxRate('Federal', 2014, 406750, 0,      .396, 'Single') )

    session.add( TaxRate('Federal', 2013, 0,      8925,   .10,  'Single') )
    session.add( TaxRate('Federal', 2013, 8925,   36250,  .15,  'Single') )
    session.add( TaxRate('Federal', 2013, 36250,  87850,  .25,  'Single') )
    session.add( TaxRate('Federal', 2013, 87850,  183250, .28,  'Single') )
    session.add( TaxRate('Federal', 2013, 183250, 398350, .33,  'Single') )
    session.add( TaxRate('Federal', 2013, 398350, 400000, .35,  'Single') )
    session.add( TaxRate('Federal', 2013, 400000, 0,      .396, 'Single') )

    session.add( TaxRate('Federal', 2014, 0,      12950,  .10,  'Head') )
    session.add( TaxRate('Federal', 2014, 12950,  49400,  .15,  'Head') )
    session.add( TaxRate('Federal', 2014, 49400,  127550, .25,  'Head') )
    session.add( TaxRate('Federal', 2014, 127550, 206600, .28,  'Head') )
    session.add( TaxRate('Federal', 2014, 206600, 405100, .33,  'Head') )
    session.add( TaxRate('Federal', 2014, 405100, 432200, .35,  'Head') )
    session.add( TaxRate('Federal', 2014, 432200, 0,      .396, 'Head') )

    session.add( TaxRate('Federal', 2013, 0,      12750,  .10,  'Head') )
    session.add( TaxRate('Federal', 2013, 12750,  48600,  .15,  'Head') )
    session.add( TaxRate('Federal', 2013, 48600,  125450, .25,  'Head') )
    session.add( TaxRate('Federal', 2013, 125450, 203150, .28,  'Head') )
    session.add( TaxRate('Federal', 2013, 203150, 398359, .33,  'Head') )
    session.add( TaxRate('Federal', 2013, 398359, 425000, .35,  'Head') )
    session.add( TaxRate('Federal', 2013, 425000, 0,      .396, 'Head') )

    session.add( TaxRate('SocialSecurity', 2013, 0, 117000, 0.062) )
    session.add( TaxRate('SocialSecurity', 2014, 0, 118500, 0.062) )

    session.add( TaxRate('Medicare', 2014, 0, 200000, 0.0145, 'Single') )
    session.add( TaxRate('Medicare', 2014, 200000, 0, 0.0235, 'Single') )
    session.add( TaxRate('Medicare', 2014, 0, 250000, 0.0145, 'Joint') )
    session.add( TaxRate('Medicare', 2014, 250000, 0, 0.0235, 'Joint') )
    session.add( TaxRate('Medicare', 2014, 0, 125000, 0.0145, 'Separate') )
    session.add( TaxRate('Medicare', 2014, 125000, 0, 0.0235, 'Separate') )

    session.commit()
