from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Book, User

engine = create_engine('sqlite:///categories_books_users.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user; Image source:  https://topgear.com.my/os/1
User1 = User(name="Sarah Carter", email="SCarter@gmail.com",
             picture='https://topgear.com.my/sites/default/files/default_images/avatar-default.png')
session.add(User1)
session.commit()

# Books for Bibles & Christianity
category1 = Category(user_id=1,
                     name="Bibles & Christianity")

session.add(category1)
session.commit()

book1 = Book(user_id=1,
             title="The Holy Bible English Standard Version (ESV)",
             price="$63.99",
             author="Crossway Bibles",
             isbn="978-1-4335-2153-9",
             category=category1)
session.add(book1)
session.commit()

book2 = Book(user_id=1,
             title="The 5 Love Languages: The Secret to Love That Lasts",
             price="$10.07",
             author="Gary Chapman",
             isbn="978-0-8024-1270-6",
             category=category1)
session.add(book2)
session.commit()

# Books for Computers
category2 = Category(user_id=1,
                     name="Computers")
session.add(category2)
session.commit()

book1 = Book(user_id=1,
              title="Python Crash Course: A Hands-On, Project-Based Introduction to Programming 1st Edition",
              price="$27.16",
              author="Eric Matthes",
              isbn="978-1-5932-7603-4",
              category=category2)
session.add(book1)
session.commit()

book2 = Book(user_id=1,
              title="Python Programming for the Absolute Beginner, Third Edition",
              price="$18.06",
              author="Michael Dawson",
              isbn="978-1-4354-5500-9",
              category=category2)
session.add(book2)
session.commit()

book3 = Book(user_id=1,
              title="HTML5 and CSS3 All-in-One For Dummies 3rd Edition",
              price="$31.59",
              author="Andy Harris",
              isbn="978-1-1182-8938-9",
              category=category2)
session.add(book3)
session.commit()

book4 = Book(user_id=1,
              title="JavaScript and JQuery: Interactive Front-End Web Development",
              price="$29.59",
              author="Jon Duckett",
              isbn="978-1-1185-3164-8",
              category=category2)
session.add(book4)
session.commit()

# Books for Cookbooks
category3 = Category(user_id=1,
                     name="Cookbooks")
session.add(category3)
session.commit()

book1 = Book(user_id=1,
              title="Cookin' Up Good Health Recipe Collection",
              price="$14.99",
              author="Donna Green-Goodman, MPH",
              isbn="978-0-9675-6402-8",
              category=category3)
session.add(book1)
session.commit()

book2 = Book(user_id=1,
              title="Ani's Raw Food Kitchen",
              price="$3.99",
              author="Ani Phyo",
              isbn="978-1-6009-4000-2",
              category=category3)
session.add(book2)
session.commit()

book3 = Book(user_id=1,
              title="7 Secrets Cookbook Healthy Cuisine Your Family Will Love",
              price="$24.99",
              author="Neva & Jim Brackett",
              isbn="978-0-8280-1995-8",
              category=category3)
session.add(book3)
session.commit()

# Books for Finance
category4 = Category(user_id=1,
                     name="Finance")
session.add(category4)
session.commit()

book1 = Book(user_id=1,
              title="Financial Peace Planner: A Step-by-Step Guide to Restoring Your Family's Financial Health",
              price="$15.55",
              author="Dave Ramsey",
              isbn="978-1-1011-9949-7",
              category=category4)
session.add(book1)
session.commit()

book2 = Book(user_id=1,
              title="Rich Dad Poor Dad: What the Rich Teach Their Kids about Money That the Poor and Middle Class Do Not!",
              price="$13.04",
              author="Robert T. Kiyosaki",
              isbn="978-1-6126-8017-0",
              category=category4)
session.add(book2)
session.commit()

book3 = Book(user_id=1,
              title="The Total Money Makeover: Classic Edition: A Proven Plan for Financial Fitness",
              price="$15.31",
              author="Dave Ramsey",
              isbn="978-1-5955-5527-4",
              category=category4)
session.add(book3)
session.commit()

# Books for Leadership
category5 = Category(user_id=1,
                     name="Leadership")
session.add(category5)
session.commit()

book1 = Book(user_id=1,
              title="The 5 Levels of Leadership: Proven Steps to Maximize Your Potential",
              price="$11.04",
              author="John C. Maxwell",
              isbn="978-1-5999-5363-2",
              category=category5)
session.add(book1)
session.commit()

book2 = Book(user_id=1,
              title="The 17 Essential Qualities of a Team Player: Becoming the Kind of Person Every Team Wants",
              price="$9.99",
              author="John C. Maxwell",
              isbn="978-1-4002-8055-1",
              category=category5)
session.add(book2)
session.commit()

book3 = Book(user_id=1,
              title="The Five Dysfunctions of a Team: A Leadership Fable",
              price="$17.22",
              author="Patrick M. Lencioni",
              isbn="978-0-7879-6075-9",
              category=category5)
session.add(book3)
session.commit()

book4 = Book(user_id=1,
              title="Good to Great: Why Some Companies Make the Leap...And Others Don't",
              price="$22.43",
              author="Jim Collins",
              isbn="978-0-0666-2099-2",
              category=category5)
session.add(book4)
session.commit()

book5 = Book(user_id=1,
             title="The 360 Degree Leader: Developing Your Influence from Anywhere in the Organization",
             price="$12.57",
             author="John C. Maxwell",
             isbn="978-1-4002-0359-8",
             category=category5)
session.add(book5)
session.commit()

print "added books!"
