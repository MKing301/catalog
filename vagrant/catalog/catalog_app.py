from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Book
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask_httpauth import HTTPBasicAuth
import httplib2
import json
from flask import make_response
import requests
from unicodedata import category

auth = HTTPBasicAuth()

app = Flask(__name__)
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Book Catalog Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///categories_books_users.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = scoped_session(DBSession)


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'], 'success')
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['facebook_id']
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'], 'success')
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()

        if login_session['provider'] == 'facebook':
            fbdisconnect()

        flash("You have successfully been logged out.", 'success')
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in to begin with!")
        return redirect(url_for('showCategories'))


# JSON API Endpoint to view all categories
@app.route('/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


# JSON API Endpoint to view all books in a category
@app.route('/category/<int:category_id>/books/JSON')
def categoryBooksJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    books = session.query(Book).filter_by(
        category_id=category_id).all()
    return jsonify(categoryBooks=[categoryBooks.serialize for categoryBooks in books])


# JSON API Endpoint to view a single book in a category
@app.route('/category/<int:category_id>/book/<int:book_id>/JSON')
def categoryBookJSON(category_id, book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    return jsonify(book=book.serialize)


# Show all categories
@app.route('/')
@app.route('/categories')
def showCategories():
    ''' Function takes no inputs, returns a list of
        all the categories form the database to the public_categories.html
        template if a user is not logged in(viewing only); otherwise, returns
        a list of all the categories to the categories.html template (edit mode),
        with the variable categories
    '''
    categories = session.query(Category).order_by(asc(Category.name))
    if 'username' not in login_session:
        return render_template('public_categories.html', categories=categories)
    else:
        return render_template('categories.html', categories=categories)


# Create a new category
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(
            name=request.form['newCategoryName'], user_id=login_session['user_id'])
        session.add(newCategory)
        flash('New Category Successfully Created', 'success')
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')


# Edit a category
@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedCategory = session.query(
        Category).filter_by(id=category_id).one()
    if editedCategory.user_id != login_session['user_id']:
        flash('You are not authorized to edit this category.', 'danger')
        return redirect(url_for('showCategories'))
    if request.method == 'POST':
        if request.form['revisedCategory']:
            editedCategory.name = request.form['revisedCategory']
            flash('Category Successfully Edited!', 'success')
            return redirect(url_for('showCategories'))
    else:
        return render_template('editCategory.html', category=editedCategory)


# Delete a category
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    if categoryToDelete.user_id != login_session['user_id']:
        flash ('You are not authorized to delete this category.', 'danger')
        return redirect(url_for('showCategories', category_id=category_id))
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        flash('Category Successfully Deleted!', 'success')
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        return render_template('deleteCategory.html', categoryToDelete=categoryToDelete, category_id=category_id)


# Show books under Category
@app.route('/category/<int:category_id>/books')
@app.route('/category/<int:category_id>')
def showBooks(category_id):
    ''' Function takes 1 input, returns the books
        for the category in book.html template with variables
        category, book and category_id
        
        input(s):
        category_id - the id of the restaurant
    '''
    category = session.query(Category).filter_by(id=category_id).one()
    books = session.query(Book).filter_by(category_id=category_id)
    if 'username' not in login_session:
        return render_template('public_book_list.html', category=category, books=books, category_id=category_id)
    else:
        return render_template('book_list.html', category=category, books=books, category_id=category_id)


# Add Book
@app.route('/category/<int:category_id>/book/new', methods=['GET', 'POST'])
def newBook(category_id):
    ''' Function takes one inputs, for post request 
        adds a new book in the database for a 
        category and redirects user to the showBooks 
        function.  For get request, returns newBook.html 
        template with variable category_id

        input(s):
        category_id - the id of the category
    '''
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newBook = Book(title=request.form['newBookTitle'],
                       price=request.form['newBookPrice'],
                       author=request.form['newBookAuthor'],
                       isbn=request.form['newBookIsbn'],
                       category_id=category_id,
                       user_id=login_session['user_id'])
        session.add(newBook)
        session.commit()
        flash('New Book Added!', 'success')
        return redirect(url_for('showBooks', category_id=category_id))
    else:
        return render_template('newBook.html', category_id=category_id)


# Edit Book
@app.route('/category/<int:category_id>/book/<int:book_id>/edit', methods=['GET', 'POST'])
def editBook(category_id, book_id):
    ''' Function takes 2 inputs. For post request,
        edits a book in the database for the 
        selected category by category id and book id, 
        then redirects user to the showBooks
        function.  For get request, returns editBook.html
        template with variables category_id , book_id and book

        input(s):
        category_id - the id of the category
        book_id - the id of the book
    '''
    if 'username' not in login_session:
        return redirect('/login')
    editedBook = session.query(Book).filter_by(id=book_id).one()
    if editedBook.user_id != login_session['user_id']:
        flash('You are not authorized to edit this book.', 'danger')
        return redirect(url_for('showBooks', category_id=category_id))
    if request.method == 'POST':
        if request.form['revisedBookTitle']:
            editedBook.title = request.form['revisedBookTitle']
        if request.form['revisedBookPrice']:
            editedBook.price = request.form['revisedBookPrice']
        if request.form['revisedBookAuthor']:
            editedBook.author = request.form['revisedBookAuthor']
        if request.form['revisedBookIsbn']:
            editedBook.isbn = request.form['revisedBookIsbn']
        session.add(editedBook)
        session.commit()
        flash('Book Successsfully Edited!', 'success')
        return redirect(url_for('showBooks', category_id=category_id))
    else:
        return render_template('editbook.html', category_id=category_id, book_id=book_id, book=editedBook)


# Delete book
@app.route('/category/<int:category_id>/book/<int:book_id>/delete', methods=['GET', 'POST'])
def deleteBook(category_id, book_id):
    ''' Function takes 2 inputs, for post request it 
        deletes a new menu item from the database for a 
        restaurant and redirects user to the showMenu 
        funtion.  For get request, returns deleteconfirmation.html 
        template with variables restaurant_id and item

        input(s):
        restaurant_id - the id of the 
        menu_id - the id of the menu item
    '''
    if 'username' not in login_session:
        return redirect('/login')
    bookToDelete = session.query(Book).filter_by(id=book_id).one()
    if bookToDelete.user_id != login_session['user_id']:
        flash ('You are not authorized to delete this book.', 'danger')
        return redirect(url_for('showBooks', category_id=category_id))
    if request.method == 'POST':
        session.delete(bookToDelete)
        session.commit()
        flash('Book Successfully Deleted!', 'success')
        return redirect(url_for('showBooks', category_id=category_id))
    else:
        return render_template('deleteBook.html', category_id=category_id, book=bookToDelete)


if __name__ == '__main__':
    app.secret_key = 'testkey123'
    app.run(host='0.0.0.0', port=5000, debug=True)
