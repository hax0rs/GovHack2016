from template import app

@app.route('/')
def index():
    return "Hello, Memes!"
