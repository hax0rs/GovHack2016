__version__ = '0.1.hack'

from flask import Flask
app = Flask(__name__)

import os

app.secret_key = os.environ.get('FLASK_SECRET_KEY', "default key")

import couchdb
server = couchdb.Server("http://admin:thememer@db:5984/")

# generate the tables if they do not exist
dbs={}
for dbname in ['uni', 'subject', 'tag', 'user', 'question']:
    if dbname not in server:
        db = server.create(dbname)
    else:
        db = server[dbname]
    dbs[dbname] = db
app.dbs = dbs

import template.views
