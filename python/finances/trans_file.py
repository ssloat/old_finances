from sqlalchemy import Column, Integer, String

from finances import Base

class TransFile(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    account = Column(String)

    def __init__(self, name, account):
        self.name = name
        self.account = account

    def __repr__(self):
       return "<TransFile('%s', '%s')>" % (self.name, self.account)


