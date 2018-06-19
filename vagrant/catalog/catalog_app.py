from flask import Flask, render_template, flash, redirect, url_for, session, request, jsonify, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.secret_key = 'testkey123'
    app.run(host='0.0.0.0', port=8000, debug=True)
