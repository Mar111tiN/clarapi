from tables import Image, Collection, User, Keyword, Base

def create_tables(engine):
    Base.metadata.create_all(engine)