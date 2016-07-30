from template import app

from flask import request, jsonify, session
import bcrypt


def logged_in():
    return True  # TODO REMOVE THIS
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

    map_email = '''function(doc) {{ if(doc.email==="{}") emit(doc._id, doc); }}'''.format(
        data['email'])
    res = list(app.dbs['user'].query(map_email))
    if len(res) != 0:
        return jsonify(**{"Error": "Email already in use"})

    hashed = bcrypt.hashpw(str.encode(data['password']), bcrypt.gensalt())
    new_record['password'] = hashed.decode("UTF-8")

    doc_id, doc_rev = app.dbs["user"].save(new_record)

    login_to(doc_id)
    return jsonify(**{"id": doc_id})


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

    map_email = '''function(doc) {{ if(doc.email==="{}") emit(doc._id, doc); }}'''.format(
        data['email'])
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

def get_tags_via(map_):
    out = []
    for row in app.dbs['tag'].query(map_):
        obj = {'id': row.value['_id'], 'text': row.value['text']}
        if 'parent' in row.value:
            obj['parent'] = row.value['parent']
        out.append(obj)
    return jsonify(*out)


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
            return jsonify(
                **{"Error": "Parents need to exist, ain't no orphans here"})
        new_record["parent"] = data["parent"]

    if "text" not in data or not data["text"]:
        return jsonify(**{"Error": "Needs a text param"})

    new_record["text"] = data["text"]
    doc_id, doc_rev = app.dbs["tag"].save(new_record)
    return jsonify(**{"id": doc_id})


@app.route('/tag/')
def get_all_tags():
    map_all = '''function(doc) {emit(doc._id, doc);}'''
    return get_tags_via(map_all)


@app.route('/tag/top')
def get_top_tags():
    map_top = '''function(doc) { if( ! doc.parent ) emit(doc._id, doc);}'''
    return get_tags_via(map_top)


@app.route('/tag/child/<tid>')
def get_child_tags(tid):
    map_child = '''function(doc) {{ if( doc.parent === "{}" ) emit(doc._id, doc);}}'''.format(
        tid)
    return get_tags_via(map_child)


@app.route('/tag/<tid>')
def get_tag(tid):
    map_tag = '''function(doc) {{ if( doc._id === "{}" ) emit(doc._id, doc);}}'''.format(
        tid)
    return get_tags_via(map_tag)

# questions


def get_questions_via(map_):
    out = []
    for row in app.dbs['question'].query(map_):
        obj = {'id': row.value['_id'], 'body': row.value['body'],
               'ans': row.value['ans'], 'tags': row.value['tags']}
        if row.value['type'] == 'mcq':
            obj['mcans'] = row.value['mcans']
        if 'exp' in row.value:
            obj['exp'] = row.value['exp']
        out.append(obj)
    return jsonify(*out)


@app.route('/question/new', methods=["POST"])
def create_new_question():
    if request.method != "POST":
        return jsonify(**{"Error": "Post my boy, POST."})

    if not logged_in():
        return jsonify(**{"Error": "You need to be logged in to do this."})

    data = request.get_json()
    if not data:
        return jsonify(**{"Error": "JSON for posting fam"})

    new_record = {}

    if "type" not in data or not data["type"]:
        return jsonify(**{"Error": "Needs a type param"})
    new_record["type"] = data["type"]

    if "body" not in data or not data["body"]:
        return jsonify(**{"Error": "Needs a body param"})
    new_record["body"] = data["body"]

    if data["type"] == "mcq":
        if "mcans" not in data or not data["mcans"]:
            return jsonify(**{"Error": "Needs a mcans param"})
        new_record["text"] = data["text"]

    if "ans" not in data or not data["ans"]:
        return jsonify(**{"Error": "Needs a ans param"})
    new_record["ans"] = data["ans"]

    if "exp" in data and data["exp"]:
        new_record["exp"] = data["exp"]

    if "tags" in data and data["tags"]:
        new_record["tags"] = data["tags"]
    else:
        new_record['tags'] = []

    doc_id, doc_rev = app.dbs["question"].save(new_record)
    return jsonify(**{"id": doc_id})


@app.route('/question/')
def get_all_questions():
    map_all = '''function(doc) {emit(doc._id, doc);}'''
    return get_questions_via(map_all)


@app.route('/question/<qid>')
def get_question(qid):
    map_quest = '''function(doc) {{ if( doc._id === "{}" ) emit(doc._id, doc);}}'''.format(
        qid)
    return get_questions_via(map_quest)


@app.route('/question/tag/<tid>')
def get_questions_tag(tid):
    map_tag = '''function(doc) {{ if( doc.tags.indexOf("{}") != -1 ) emit(doc._id, doc);}}'''.format(tid)
    return get_questions_via(map_tag)


@app.route('/question/tag/children/<tid>')
def get_questions_tag_and_children(tid):
    map_tag = '''function(doc) {{ if( doc.tags.indexOf("{}") != -1 ) emit(doc._id, doc);}}'''.format(tid)
    return get_questions_via(map_tag)


# TODO make efficent at some point
@app.route('/question/subject/<sid>')
def get_questions_subject(sid):
    map_sub = '''function(doc) {{ if(doc._id==="{}") emit(doc._id, doc); }}'''.format(
        sid)
    res = list(app.dbs['subject'].query(map_sub))
    if len(res) != 1:
        return jsonify(**{"Error": "Subject is invalid"})
    tags = res[0].value['tags']
    map_stag = '''function(doc) {{ for each (tag in {}) {{if( doc.tags.indexOf(tag) != -1 ) {{emit(doc._id, doc); break; }} }} }}'''.format(
        tags)
    return get_questions_via(map_stag)


# subjects


def get_subjects_via(map_):
    out = []
    for row in app.dbs['subject'].query(map_):
        obj = {
            'id': row.value['_id'],
            'name': row.value['name'],
            'uni': row.value['uni']}
        if 'tags' in row.value:
            obj['tags'] = row.value['tags']
        out.append(obj)
    return jsonify(*out)


@app.route('/subject/new', methods=["POST"])
def create_new_subject():
    if request.method != "POST":
        return jsonify(**{"Error": "Post my boy, POST."})

    if not logged_in():
        return jsonify(**{"Error": "You need to be logged in to do this."})

    data = request.get_json()
    if not data:
        return jsonify(**{"Error": "JSON for posting fam"})

    new_record = {}

    if "name" not in data or not data["name"]:
        return jsonify(**{"Error": "Needs a name param"})
    new_record["name"] = data["name"]

    if "uni" not in data or not data["uni"]:
        return jsonify(**{"Error": "Needs a uni param"})
    new_record["uni"] = data["uni"]

    if "tags" not in data or not data["tags"]:
        return jsonify(**{"Error": "Needs a tags param"})
    new_record["tags"] = data["tags"]

    doc_id, doc_rev = app.dbs["subject"].save(new_record)
    return jsonify(**{"id": doc_id})


@app.route('/subject/')
def get_all_subjects():
    map_all = '''function(doc) {emit(doc._id, doc);}'''
    return get_subjects_via(map_all)


@app.route('/subject/<sid>')
def get_subject(sid):
    map_sub = '''function(doc) {{ if( doc._id === "{}" ) emit(doc._id, doc);}}'''.format(
        sid)
    return get_subjects_via(map_sub)


@app.route('/subject/uni/<uni>')
def get_subjects_uni(uni):
    map_uni = '''function(doc) {{ if( doc.uni === "{}" ) emit(doc._id, doc);}}'''.format(
        uni)
    return get_subjects_via(map_uni)
