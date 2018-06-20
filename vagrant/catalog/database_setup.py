from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
       }


class Book(Base):
    __tablename__ = 'book'

    title = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    price = Column(String(8))
    author = Column(String(80))
    isbn = Column(String(17))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'title'         : self.title,
           'price'         : self.price,
           'id'         : self.id,
           'author'         : self.author,
           'isbn'         : self.isbn,
       }


engine = create_engine('sqlite:///categories_books_users.db')

Base.metadata.create_all(engine)
