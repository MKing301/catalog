from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    '''A user of the catalog app program. Users will have
       the following attributes:
       Attibute(s):
       id - unique id number for each user
       name - user's name
       email - user's email address
       picture - user's picture
    '''
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    '''A category for the books in the catalog app program. Categories
       will have the following attributes:
       Attibute(s):
       id - unique id number
       user_id - id of user that created the category
    '''
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        '''Return category object data in easily serializeable format'''
        return {
           'name': self.name,
           'id': self.id,
        }


class Book(Base):
    '''A book in the catalog app program. Books will have
       the following attributes:
       Attibute(s):
       title - title of the book
       id - unique id number for each book
       price - price of the book
       author - author of the book
       isbn - isbn for the book
       category_id - id of the category the book is located
       user_id - id of user that created the book
    '''
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
        '''Return book object data in easily serializeable format'''
        return {
           'title': self.title,
           'price': self.price,
           'id': self.id,
           'author': self.author,
           'isbn': self.isbn,
        }


engine = create_engine('sqlite:///categories_books_users.db')

Base.metadata.create_all(engine)
