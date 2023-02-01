from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import *


def get_engine(echo=False):
    url = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    engine = create_engine(url, echo=echo)
    return engine


def get_session(echo=False):
    engine = get_engine(echo)
    session = sessionmaker(bind=engine)
    return session


