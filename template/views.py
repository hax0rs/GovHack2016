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

"""
@api {POST} /user/new Create a new user.
@apiName NewUser
@apiGroup User

@apiDescription Attempts to create a new user and log them
    in, returning an error if unsuccesful

@apiExample {curl} CURL
curl -X POST -H "Content-Type: application/json" -d '{"email": "Test@example.com", "name": "Nicolaus", "password": "pa$$w0RD"}' http://localhost/user/new

@apiExample {json} JSON
    {
        "email": "Test@example.com",
        "name": "Nicolaus",
        "password": "pa$$w0RD"
    }
"""


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


"""
@api {POST} /user/login Logs a user in
@apiName LoginUser
@apiGroup User

@apiDescription Attempts to log the user in, returning
    an error if unsuccesful

@apiExample {curl} CURL
curl -X POST -H "Content-Type: application/json" -d '{"email": "Test@example.com", "password": "pa$$w0RD"}' http://localhost/user/login

@apiExample {json} JSON
    {
        "email": "Test@example.com",
        "password": "pa$$w0RD"
    }
"""


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


"""
@api {GET} /user/logout Logs the current user out
@apiName LogoutUser
@apiGroup User

@apiDescription Logs the current user out if one
    logged in, returning an error if one is not

@apiExample {curl} Logout current user
    curl http://127.0.0.1:5000/user/logout

@apiSuccessExample {json} Success-Response:
    {
        "Status": "You are logged out"
    }
"""


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


"""
@api {POST} /tag/new Create a new tag.
@apiName NewTag
@apiGroup Tags

@apiExample {curl} CURL
    curl -X POST -H "Content-Type: application/json" -d '{"text": "Computing"}' http://localhost/tag/new

@apiExample {json} JSON
    {
        "text": "Computing"
    }

"""


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

"""
@api {GET} /tag/ Get all tags
@apiName GetAllTags
@apiGroup Tags

@apiDescription Returns all the tags, even child
    tags

@apiExample {curl} Get all tags
    curl http://127.0.0.1:5000/tag/

@apiSuccessExample {json} Success-Response:
    [
        {
            "id": "7b5cdd934757e92748787b8ed4000f5d",
            "text": "Computing"
        },
        {
            "id": "7b5cdd934757e92748787b8ed4001949",
            "parent": "7b5cdd934757e92748787b8ed4000f5d",
            "text": "Linux"
        }
    ]

"""


@app.route('/tag/')
def get_all_tags():
    map_all = '''function(doc) {emit(doc._id, doc);}'''
    return get_tags_via(map_all)


"""
@api {GET} /tag/top Get all the top level tags
@apiName GetAllTopTags
@apiGroup Tags

@apiDescription Returns all the tags which do not have
    parents and as such are root nodes on the tag tree

@apiExample {curl} Get all top tags
    curl http://127.0.0.1:5000/tag/top

@apiSuccessExample {json} Success-Response:
    [
        {
            "id": "7b5cdd934757e92748787b8ed4000f5d",
            "text": "Computing"
        }
    ]
"""


@app.route('/tag/top')
def get_top_tags():
    map_top = '''function(doc) { if( ! doc.parent ) emit(doc._id, doc);}'''
    return get_tags_via(map_top)


"""
@api {GET} /tag/child/<tag_id> Get all child tags of a certain tag
@apiName GetAllChildTags
@apiGroup Tags
@apiParam {String} tag_id The id of the parent tag

@apiDescription Returns all the tags which parent tag
    is passed in the param

@apiExample {curl} Get all child tags of a root tag
    curl http://127.0.0.1:5000/tag/child/7b5cdd934757e92748787b8ed4000f5d

@apiSuccessExample {json} Success-Response:
    [
        {
            "id": "7b5cdd934757e92748787b8ed4001949",
            "parent": "7b5cdd934757e92748787b8ed4000f5d",
            "text": "Linux"
        }
    ]
"""


@app.route('/tag/child/<tid>')
def get_child_tags(tid):
    map_child = '''function(doc) {{ if( doc.parent === "{}" ) emit(doc._id, doc);}}'''.format(
        tid)
    return get_tags_via(map_child)


"""
@api {GET} /tag/<tag_id> Get info on a certain tag
@apiName GetTag
@apiGroup Tags
@apiParam {String} tag_id The id of the tag

@apiDescription Returns info on the selected tag

@apiExample {curl} Get all child tags of a root tag
    curl http://127.0.0.1:5000/tag/7b5cdd934757e92748787b8ed4000f5d

@apiSuccessExample {json} Success-Response:
    [
        {
            "id": "7b5cdd934757e92748787b8ed4000f5d",
            "text": "Computing"
        }
    ]
"""


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
               'ans': row.value['ans'], 'tags': row.value['tags'],
               'author': row.value['author']}
        if row.value['type'] == 'mcq':
            obj['mcans'] = row.value['mcans']
        if 'exp' in row.value:
            obj['exp'] = row.value['exp']
        out.append(obj)
    return jsonify(*out)

"""
@api {POST} /question/new Create a new question.
@apiName NewQuestion
@apiGroup Questions

@apiExample {curl} CURL
    curl -X POST -H "Content-Type: application/json" -d '{"type": "text", "body": "What is a spicy boi?", "ans": "A fireant", "exp": "Spicy boi > hot animal > fire ant", "tags": ["7b5cdd934757e92748787b8ed4000f5d", "7b5cdd934757e92748787b8ed4001949"]}' http://localhost/question/new

@apiExample {json} JSON
    {
        "type": "text",
        "body": "What is a spicy boi?",
        "ans": "A fireant", "exp": "Spicy boi > hot animal > fire ant",
        "tags": ["7b5cdd934757e92748787b8ed4000f5d", "7b5cdd934757e92748787b8ed4001949"]
    }

"""


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
    new_record['author'] = session['id']

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

"""
@api {GET} /question/ Get questions.
@apiName GetQuestions
@apiGroup Questions

@apiDescription Returns all the available questions.

@apiExample {curl} CURL
    curl http://127.0.0.1:5000/question/
"""


@app.route('/question/')
def get_all_questions():
    map_all = '''function(doc) {emit(doc._id, doc);}'''
    return get_questions_via(map_all)

"""
@api {GET} /question/<question_id> Get question by ID.
@apiName GetQuestionByID
@apiGroup Questions

@apiExample {curl} CURL
    curl http://127.0.0.1:5000/question/b53e73f5422f46aabbe91fb6b2001642

@apiSuccessExample {json} Success-Response:
{
  "ans": "A fireant",
  "body": "What is a spicy boi?",
  "exp": "Spicy boi > hot animal > fire ant",
  "id": "b53e73f5422f46aabbe91fb6b2001642",
  "tags": [
    "7b5cdd934757e92748787b8ed4000f5d",
    "7b5cdd934757e92748787b8ed4001949"
  ]
}
"""


@app.route('/question/<qid>')
def get_question(qid):
    map_quest = '''function(doc) {{ if( doc._id === "{}" ) emit(doc._id, doc);}}'''.format(
        qid)
    return get_questions_via(map_quest)


"""
@api {GET} /question/tag/<tag_id> Get questions by tag.
@apiName GetQuestionByTag
@apiGroup Questions

@apiParam {String} tag_id The tag id to search with

@apiDescription Returns all the questions that contain
    the given tag.

@apiExample {curl} CURL
    curl http://127.0.0.1:5000/question/tag/7b5cdd934757e92748787b8ed4000f5d
"""


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

"""
@api {POST} /subject/new Creates a new subject.
@apiName NewSubject
@apiGroup Subject

@apiExample {curl} Create new subject:
    curl -X POST -H "Content-Type: application/json" -d '{"name":"csse2310", "uni":"UQ", "tags": ["7b5cdd934757e92748787b8ed4000f5d", "7b5cdd934757e92748787b8ed4001949"]}' http://localhost/subject/new
"""


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

"""
@api {GET} /subject/ Returns list of subjects
@apiName GetSubjects
@apiGroup Subject

@apiExample {curl} Get subjects
    curl http://127.0.0.1:5000/subject/
"""


@app.route('/subject/')
def get_all_subjects():
    map_all = '''function(doc) {emit(doc._id, doc);}'''
    return get_subjects_via(map_all)

"""
@api {GET} /subject/<subject_id> Get subject details.
@apiName GetSubjectInfo
@apiGroup Subject
@apiParam {String} subject_id The subject identifier.

@apiDescription Returns the details of the specified subject.

@apiExample {curl} Get subject details via ID
    curl http://127.0.0.1:5000/subject/b53e73f5422f46aabbe91fb6b2000429

@apiSuccessExample {json} Success-Response:
    {
      "id": "b53e73f5422f46aabbe91fb6b2000429",
      "name": "csse2310",
      "tags": [
        "7b5cdd934757e92748787b8ed4000f5d",
        "7b5cdd934757e92748787b8ed4001949"
      ],
      "uni": "UQ"
    }
"""


@app.route('/subject/<sid>')
def get_subject(sid):
    map_sub = '''function(doc) {{ if( doc._id === "{}" ) emit(doc._id, doc);}}'''.format(
        sid)
    return get_subjects_via(map_sub)


"""
@api {GET} /subject/uni/<uni_id> Uni Subjects
@apiName GetUniSubjects
@apiGroup Subject
@apiParam {String} uni The identifier for the specified
    university.

@apiDescription Returns all the subjects available
    at a given uni.

@apiExample {curl} Get all subjects at a given uni
    curl http://127.0.0.1:5000/subject/uni/UQ

@apiSuccessExample {json} Success-Response:
    [
        {
        "id": "b53e73f5422f46aabbe91fb6b2000429",
        "name": "csse2310",
        "tags": [
        "7b5cdd934757e92748787b8ed4000f5d",
        "7b5cdd934757e92748787b8ed4001949"
        ],
            "uni": "UQ"
        },
        {
        "id": "b53e73f5422f46aabbe91fb6b2001124",
        "name": "csse2310",
        "tags": [
            "7b5cdd934757e92748787b8ed4000f5d",
            "7b5cdd934757e92748787b8ed4001949"
        ],
        "uni": "UQ"
        }
    ]
"""


@app.route('/subject/uni/<uni>')
def get_subjects_uni(uni):
    map_uni = '''function(doc) {{ if( doc.uni === "{}" ) emit(doc._id, doc);}}'''.format(
        uni)
    return get_subjects_via(map_uni)
