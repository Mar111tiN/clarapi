from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean, Table
from sqlalchemy.orm import relationship
from db import Base

image_keywords_association = Table('association', Base.metadata, 
                                   Column('img_id', Integer, ForeignKey('images.id')),
                                   Column('key_id', Integer, ForeignKey('keywords.id')))

class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    title = Column(String(90))
    path = Column(String(80), nullable=False)
    date = Column(Date(), nullable=False)
    date_assumed = Column(Boolean(), nullable=True)
    note = Column(String(120))
    helper = Column(String(80))
    stars = Column(Integer())
    
    col_id = Column(Integer, ForeignKey('collections.id'))
    collection = relationship("Collection", back_populates='images')
    
    user_id = Column(Integer, ForeignKey('users.id'))
    artist = relationship('User', back_populates='images')
    
    key_id = Column(Integer, ForeignKey('keywords.id'))
    # here, backref is used to create an images field in the Keyword table
    keywords = relationship('Keyword', secondary=image_keywords_association, backref='images')
    
    def __repr__(self):
        return f'<Image("{self.title}" by {self.artist.name}, ~/{self.path})>'

    
class Collection(Base):
    __tablename__ = 'collections'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    images = relationship('Image', back_populates='collection')

    def __repr__(self):
        return f"<Collection(name:{self.name}, images:{len(self.images)})>"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    types = Column(String(50))
    age = Column(Integer)
    images = relationship('Image', back_populates='artist')
    
    def __repr__(self):
        return f"<User(name:{self.name}, age:{self.age}, images:{len(self.images)})>"
    
    
class Keyword(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    
    def __repr__(self):
        return f"<Keyword(name={self.name}, images:{len(self.images)})>"
