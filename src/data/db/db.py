from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import database_name, database_pw

engine = None
Session = None
Base = declarative_base()


def get_engine():
    global engine
    if engine is None:
        engine = create_engine('postgresql://' + database_name + ':' + database_pw + '@localhost:5432/')
    return engine


def get_session():
    global Session
    if Session is None:
        Session = sessionmaker(bind=engine)
    return Session

