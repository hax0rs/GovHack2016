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

## create the views
#views = [('question', {
#  "_id":"_design/views",
#  "language": "javascript",
#  "views":
#  {
#    "all": {
#      "map": "function(doc) { emit(null, doc) }"
#    },
#    "by_id": {
#      "map": "function(doc) { emit(doc._id, doc) }"
#    },
#    "by_tag": {
#      "map": "function(doc) { for each (tag in doc.tags) { emit(tag, doc) } }"
#    }
#  }
#})]
#
#for view_ in views:
#    db, view = view_
#    app.dbs[db].save(view)
#    # dw about overiding, it is set rev

import template.views
