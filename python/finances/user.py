from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
       return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine) 

Session = sessionmaker(bind=engine)
session = Session()

u = User('steve', 'stephen', '1234')
session.add(u)

q = session.query(User).filter_by(name='steve').first()
print q
