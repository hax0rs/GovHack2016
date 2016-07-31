define({ "api": [
  {
    "type": "GET",
    "url": "/question/<question_id>",
    "title": "Get question by ID.",
    "name": "GetQuestionByID",
    "group": "Questions",
    "examples": [
      {
        "title": "CURL",
        "content": "curl http://127.0.0.1:5000/question/b53e73f5422f46aabbe91fb6b2001642",
        "type": "curl"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n  \"ans\": \"A fireant\",\n  \"body\": \"What is a spicy boi?\",\n  \"exp\": \"Spicy boi > hot animal > fire ant\",\n  \"id\": \"b53e73f5422f46aabbe91fb6b2001642\",\n  \"tags\": [\n    \"7b5cdd934757e92748787b8ed4000f5d\",\n    \"7b5cdd934757e92748787b8ed4001949\"\n  ]\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "template/views.py",
    "groupTitle": "Questions"
  },
  {
    "type": "GET",
    "url": "/question/tag/<tag_id>",
    "title": "Get questions by tag.",
    "name": "GetQuestionByTag",
    "group": "Questions",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tag_id",
            "description": "<p>The tag id to search with</p>"
          }
        ]
      }
    },
    "description": "<p>Returns all the questions that contain the given tag.</p>",
    "examples": [
      {
        "title": "CURL",
        "content": "curl http://127.0.0.1:5000/question/tag/7b5cdd934757e92748787b8ed4000f5d",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "template/views.py",
    "groupTitle": "Questions"
  },
  {
    "type": "GET",
    "url": "/question/",
    "title": "Get questions.",
    "name": "GetQuestions",
    "group": "Questions",
    "description": "<p>Returns all the available questions.</p>",
    "examples": [
      {
        "title": "CURL",
        "content": "curl http://127.0.0.1:5000/question/",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "template/views.py",
    "groupTitle": "Questions"
  },
  {
    "type": "POST",
    "url": "/question/new",
    "title": "Create a new question.",
    "name": "NewQuestion",
    "group": "Questions",
    "examples": [
      {
        "title": "CURL",
        "content": "curl -X POST -H \"Content-Type: application/json\" -d '{\"type\": \"text\", \"body\": \"What is a spicy boi?\", \"ans\": \"A fireant\", \"exp\": \"Spicy boi > hot animal > fire ant\", \"tags\": [\"7b5cdd934757e92748787b8ed4000f5d\", \"7b5cdd934757e92748787b8ed4001949\"]}' http://localhost/question/new",
        "type": "curl"
      },
      {
        "title": "JSON",
        "content": "{\n    \"type\": \"text\",\n    \"body\": \"What is a spicy boi?\",\n    \"ans\": \"A fireant\", \"exp\": \"Spicy boi > hot animal > fire ant\",\n    \"tags\": [\"7b5cdd934757e92748787b8ed4000f5d\", \"7b5cdd934757e92748787b8ed4001949\"]\n}",
        "type": "json"
      }
    ],
    "version": "0.0.0",
    "filename": "template/views.py",
    "groupTitle": "Questions"
  },
  {
    "type": "GET",
    "url": "/subject/<subject_id>",
    "title": "Get subject details.",
    "name": "GetSubjectInfo",
    "group": "Subject",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "subject_id",
            "description": "<p>The subject identifier.</p>"
          }
        ]
      }
    },
    "description": "<p>Returns the details of the specified subject.</p>",
    "examples": [
      {
        "title": "Get subject details via ID",
        "content": "curl http://127.0.0.1:5000/subject/b53e73f5422f46aabbe91fb6b2000429",
        "type": "curl"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n  \"id\": \"b53e73f5422f46aabbe91fb6b2000429\",\n  \"name\": \"csse2310\",\n  \"tags\": [\n    \"7b5cdd934757e92748787b8ed4000f5d\",\n    \"7b5cdd934757e92748787b8ed4001949\"\n  ],\n  \"uni\": \"UQ\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "template/views.py",
    "groupTitle": "Subject"
  },
  {
    "type": "GET",
    "url": "/subject/",
    "title": "Returns list of subjects",
    "name": "GetSubjects",
    "group": "Subject",
    "examples": [
      {
        "title": "Get subjects",
        "content": "curl http://127.0.0.1:5000/subject/",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "template/views.py",
    "groupTitle": "Subject"
  },
  {
    "type": "GET",
    "url": "/subject/uni/<uni_id>",
    "title": "Uni Subjects",
    "name": "GetUniSubjects",
    "group": "Subject",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "uni",
            "description": "<p>The identifier for the specified university.</p>"
          }
        ]
      }
    },
    "description": "<p>Returns all the subjects available at a given uni.</p>",
    "examples": [
      {
        "title": "Get all subjects at a given uni",
        "content": "curl http://127.0.0.1:5000/subject/uni/UQ",
        "type": "curl"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "[\n    {\n    \"id\": \"b53e73f5422f46aabbe91fb6b2000429\",\n    \"name\": \"csse2310\",\n    \"tags\": [\n    \"7b5cdd934757e92748787b8ed4000f5d\",\n    \"7b5cdd934757e92748787b8ed4001949\"\n    ],\n        \"uni\": \"UQ\"\n    },\n    {\n    \"id\": \"b53e73f5422f46aabbe91fb6b2001124\",\n    \"name\": \"csse2310\",\n    \"tags\": [\n        \"7b5cdd934757e92748787b8ed4000f5d\",\n        \"7b5cdd934757e92748787b8ed4001949\"\n    ],\n    \"uni\": \"UQ\"\n    }\n]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "template/views.py",
    "groupTitle": "Subject"
  },
  {
    "type": "POST",
    "url": "/subject/new",
    "title": "Creates a new subject.",
    "name": "NewSubject",
    "group": "Subject",
    "examples": [
      {
        "title": "Create new subject:",
        "content": "curl -X POST -H \"Content-Type: application/json\" -d '{\"name\":\"csse2310\", \"uni\":\"UQ\", \"tags\": [\"7b5cdd934757e92748787b8ed4000f5d\", \"7b5cdd934757e92748787b8ed4001949\"]}' http://localhost/subject/new",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "template/views.py",
    "groupTitle": "Subject"
  },
  {
    "type": "GET",
    "url": "/tag/child/<tag_id>",
    "title": "Get all child tags of a certain tag",
    "name": "GetAllChildTags",
    "group": "Tags",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tag_id",
            "description": "<p>The id of the parent tag</p>"
          }
        ]
      }
    },
    "description": "<p>Returns all the tags which parent tag is passed in the param</p>",
    "examples": [
      {
        "title": "Get all child tags of a root tag",
        "content": "curl http://127.0.0.1:5000/tag/child/7b5cdd934757e92748787b8ed4000f5d",
        "type": "curl"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "[\n    {\n        \"id\": \"7b5cdd934757e92748787b8ed4001949\",\n        \"parent\": \"7b5cdd934757e92748787b8ed4000f5d\",\n        \"text\": \"Linux\"\n    }\n]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "template/views.py",
    "groupTitle": "Tags"
  },
  {
    "type": "GET",
    "url": "/tag/",
    "title": "Get all tags",
    "name": "GetAllTags",
    "group": "Tags",
    "description": "<p>Returns all the tags, even child tags</p>",
    "examples": [
      {
        "title": "Get all tags",
        "content": "curl http://127.0.0.1:5000/tag/",
        "type": "curl"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "[\n    {\n        \"id\": \"7b5cdd934757e92748787b8ed4000f5d\",\n        \"text\": \"Computing\"\n    },\n    {\n        \"id\": \"7b5cdd934757e92748787b8ed4001949\",\n        \"parent\": \"7b5cdd934757e92748787b8ed4000f5d\",\n        \"text\": \"Linux\"\n    }\n]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "template/views.py",
    "groupTitle": "Tags"
  },
  {
    "type": "GET",
    "url": "/tag/top",
    "title": "Get all the top level tags",
    "name": "GetAllTopTags",
    "group": "Tags",
    "description": "<p>Returns all the tags which do not have parents and as such are root nodes on the tag tree</p>",
    "examples": [
      {
        "title": "Get all top tags",
        "content": "curl http://127.0.0.1:5000/tag/top",
        "type": "curl"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "[\n    {\n        \"id\": \"7b5cdd934757e92748787b8ed4000f5d\",\n        \"text\": \"Computing\"\n    }\n]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "template/views.py",
    "groupTitle": "Tags"
  },
  {
    "type": "GET",
    "url": "/tag/<tag_id>",
    "title": "Get info on a certain tag",
    "name": "GetTag",
    "group": "Tags",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tag_id",
            "description": "<p>The id of the tag</p>"
          }
        ]
      }
    },
    "description": "<p>Returns info on the selected tag</p>",
    "examples": [
      {
        "title": "Get all child tags of a root tag",
        "content": "curl http://127.0.0.1:5000/tag/7b5cdd934757e92748787b8ed4000f5d",
        "type": "curl"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "[\n    {\n        \"id\": \"7b5cdd934757e92748787b8ed4000f5d\",\n        \"text\": \"Computing\"\n    }\n]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "template/views.py",
    "groupTitle": "Tags"
  },
  {
    "type": "POST",
    "url": "/tag/new",
    "title": "Create a new tag.",
    "name": "NewTag",
    "group": "Tags",
    "examples": [
      {
        "title": "CURL",
        "content": "curl -X POST -H \"Content-Type: application/json\" -d '{\"text\": \"Computing\"}' http://localhost/tag/new",
        "type": "curl"
      },
      {
        "title": "JSON",
        "content": "{\n    \"text\": \"Computing\"\n}",
        "type": "json"
      }
    ],
    "version": "0.0.0",
    "filename": "template/views.py",
    "groupTitle": "Tags"
  },
  {
    "type": "POST",
    "url": "/user/login",
    "title": "Logs a user in",
    "name": "LoginUser",
    "group": "User",
    "description": "<p>Attempts to log the user in, returning an error if unsuccesful</p>",
    "examples": [
      {
        "title": "CURL",
        "content": "curl -X POST -H \"Content-Type: application/json\" -d '{\"email\": \"Test@example.com\", \"password\": \"pa$$w0RD\"}' http://localhost/user/login",
        "type": "curl"
      },
      {
        "title": "JSON",
        "content": "{\n    \"email\": \"Test@example.com\",\n    \"password\": \"pa$$w0RD\"\n}",
        "type": "json"
      }
    ],
    "version": "0.0.0",
    "filename": "template/views.py",
    "groupTitle": "User"
  },
  {
    "type": "GET",
    "url": "/user/logout",
    "title": "Logs the current user out",
    "name": "LogoutUser",
    "group": "User",
    "description": "<p>Logs the current user out if one logged in, returning an error if one is not</p>",
    "examples": [
      {
        "title": "Logout current user",
        "content": "curl http://127.0.0.1:5000/user/logout",
        "type": "curl"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"Status\": \"You are logged out\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "template/views.py",
    "groupTitle": "User"
  },
  {
    "type": "POST",
    "url": "/user/new",
    "title": "Create a new user.",
    "name": "NewUser",
    "group": "User",
    "description": "<p>Attempts to create a new user and log them in, returning an error if unsuccesful</p>",
    "examples": [
      {
        "title": "CURL",
        "content": "curl -X POST -H \"Content-Type: application/json\" -d '{\"email\": \"Test@example.com\", \"name\": \"Nicolaus\", \"password\": \"pa$$w0RD\"}' http://localhost/user/new",
        "type": "curl"
      },
      {
        "title": "JSON",
        "content": "{\n    \"email\": \"Test@example.com\",\n    \"name\": \"Nicolaus\",\n    \"password\": \"pa$$w0RD\"\n}",
        "type": "json"
      }
    ],
    "version": "0.0.0",
    "filename": "template/views.py",
    "groupTitle": "User"
  }
] });
