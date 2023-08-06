from flask import Flask

app = Flask(__name__)


@app.route("/login")
# POST /login
def login():
    return "Login"


@app.route("/match")
# POST /match
def match():
    return "Match"


@app.route("/pull")
# GET /pull
def pull():
    return "Pull"


@app.route("/push")
# POST /push
def push():
    return "Push"


@app.route("/")
def hello():
    return "Hello, World!"
