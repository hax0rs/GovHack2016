from template import app

from flask import request, jsonify, session
import bcrypt

def logged_in():
    return ('id' in session)

def login_to(id):
    session['id'] = id

@app.route('/')
def index():
    abc = ""
    map_all = '''function(doc) {emit(doc._id, doc);}'''
    for i in app.dbs:
        abc += "<p><b>Table: {}</b></p>".format(i)
        for row in app.dbs[i].query(map_all):
            abc += "<p>{}</p>".format(row.value)
    return "Hello, Memes! {}".format(abc)

# account management

@app.route('/user/new', methods=["POST"])
def create_new_user():
    if request.method != "POST":
        return jsonify(**{"Error": "Post my boy, POST."})

    if logged_in():
        return jsonify(**{"Error": "You are logged in."})

    data = request.get_json()
    if not data:
        return jsonify(**{"Error": "JSON for posting fam"})

    new_record = {}

    # TODO one person per email

    if "email" not in data or not data["email"]:
        return jsonify(**{"Error": "Needs a email param"})
    new_record['email'] = data['email']

    if "name" not in data or not data["name"]:
        return jsonify(**{"Error": "Needs a name param"})
    new_record['name'] = data['name']

    if "password" not in data or not data["password"]:
        return jsonify(**{"Error": "Needs a password param"})

    map_email = '''function(doc) {{ if(doc.email==="{}") emit(doc._id, doc); }}'''.format(data['email'])
    res = list(app.dbs['user'].query(map_email))
    if len(res) != 0:
        return jsonify(**{"Error": "Email already in use"})

    hashed = bcrypt.hashpw(str.encode(data['password']), bcrypt.gensalt())
    new_record['password'] = hashed.decode("UTF-8")

    doc_id, doc_rev = app.dbs["user"].save(new_record)

    login_to(doc_id)
    return jsonify(**{"id" : doc_id})

@app.route('/user/login', methods=['POST'])
def login():
    if request.method != "POST":
        return jsonify(**{"Error": "Post my boy, POST."})

    if logged_in():
        return jsonify(**{"Error": "You are already logged in"})

    data = request.get_json()
    if not data:
        return jsonify(**{"Error": "JSON for posting fam"})

    if "email" not in data or not data["email"]:
        return jsonify(**{"Error": "Needs a email param"})

    if "password" not in data or not data["password"]:
        return jsonify(**{"Error": "Needs a password param"})

    map_email = '''function(doc) {{ if(doc.email==="{}") emit(doc._id, doc); }}'''.format(data['email'])
    res = list(app.dbs['user'].query(map_email))
    if len(res) != 1:
        return jsonify(**{"Error": "Invalid email"})
    account = res[0]

    hashed = str.encode(account.value['password'])
    passed = str.encode(data['password'])
    if bcrypt.hashpw(passed, hashed) != hashed:
        return jsonify(**{"Error": "Incorrect password"})

    login_to(account.key)
    return jsonify(**{"Status": "You are logged in, keep those cookies"})

@app.route('/user/logout')
def logout():
    if not logged_in():
        return jsonify(**{"Error": "You are already logged out"})
    session['id'] = None
    return jsonify(**{"Status": "You are logged out"})


# tags

@app.route('/tag/new', methods=["POST"])
def create_new_tag():
    if request.method != "POST":
        return jsonify(**{"Error": "Post my boy, POST."})

    if not logged_in():
        return jsonify(**{"Error": "You need to be logged in to do this."})

    data = request.get_json()
    if not data:
        return jsonify(**{"Error": "JSON for posting fam"})

    new_record = {}

    if "parent" in data and data["parent"]:
        if data["parent"] not in app.dbs["tag"]:
            return jsonify(**{"Error": "Parents need to exist, ain't no orphans here"})
        new_record["parent"] = data["parent"]

    if "text" not in data or not data["text"]:
        return jsonify(**{"Error": "Needs a text param"})

    new_record["text"] = data["text"]
    doc_id, doc_rev = app.dbs["tag"].save(new_record)
    return jsonify(**{"id" : doc_id})

@app.route('/tag/')
def get_all_tags():
    map_all = '''function(doc) {emit(doc._id, doc);}'''
    out = []
    for row in app.dbs['tag'].query(map_all):
        obj = {'id': row.value['_id'], 'text': row.value['text']}
        if 'parent' in row.value:
            obj['parent'] = row.value['parent']
        out.append(obj)
    return jsonify(*out)

@app.route('/tag/top')
def get_top_tags():
    map_top = '''function(doc) { if( ! doc.parent ) emit(doc._id, doc);}'''
    out = []
    for row in app.dbs['tag'].query(map_top):
        out.append({'id': row.value['_id'], 'text': row.value['text']})
    return jsonify(*out)

@app.route('/tag/child/<tid>')
def get_child_tags(tid):
    map_child = '''function(doc) {{ if( doc.parent === "{}" ) emit(doc._id, doc);}}'''.format(tid)
    out = []
    for row in app.dbs['tag'].query(map_child):
        out.append({'id': row.value['_id'], 'text': row.value['text'], 'parent': tid})
    return jsonify(*out)

@app.route('/tag/<tid>')
def get_tag(tid):
    map_tag = '''function(doc) {{ if( doc._id === "{}" ) emit(doc._id, doc);}}'''.format(tid)
    out = []
    for row in app.dbs['tag'].query(map_tag):
        obj = {'id': tid, 'text': row.value['text']}
        if 'parent' in row.value:
            obj['parent'] = row.value['parent']
        out.append(obj)
    return jsonify(*out)

# questions


