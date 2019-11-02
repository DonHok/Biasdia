from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import database_name, database_pw, database_port

engine = None
Session = None
session = None
Base = declarative_base()


def get_engine():
    global engine
    if engine is None:
        engine = create_engine('postgresql://' + database_name + ':' + database_pw
                               + '@localhost:' + str(database_port) + '/')
        Base.metadata.create_all(engine)
    return engine


def get_session():
    global Session, session
    if Session is None:
        Session = sessionmaker(bind=engine)
        Session.configure(bind=engine)
        session = Session()
    return session

