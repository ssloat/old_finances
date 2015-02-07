from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#engine = create_engine('sqlite:///:memory:', echo=True)
#engine = create_engine('sqlite:///finances.db', echo=True)

#Session = sessionmaker(bind=engine)
Session = sessionmaker()
#session = Session()

