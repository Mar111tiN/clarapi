from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


def psql_engine(dbuser, db, port=5432):
    '''
    creates postgreSQL engine and connects it to database
    '''

    engine = create_engine(f'postgresql://{dbuser}@localhost:{port}/{db}', echo=False)
    engine.connect()
    return engine


def make_session(engine):
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()
