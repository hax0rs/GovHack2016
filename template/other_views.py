from template import app

@app.route('/swag')
@app.route('/swag/')
def index():
    return "Hello, Swag!"
