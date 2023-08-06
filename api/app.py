"""
This file contains the API endpoints for the game
"""

from flask import Flask

app = Flask(__name__)


@app.route("/register")
# POST /register
def register():
    """
    Registers the user in the database
        * Return        : 200 OK if the user has been registered successfully
        * Param         : username, password, email
    """
    return "Register"


@app.route("/login")
# POST /login
def login():
    """
    Logs the user in
        * Return        : 200 OK if the user has been logged in successfully or
        401 Unauthorized if the user is not registered
        * Param         : username, password
    """
    return "Login"


@app.route("/match")
# POST /match
def match():
    """
    Start a new game with the given user and the logged in user
        * Return        : 200 OK if the game has been started successfully or
        401 Unauthorized (multiple reasons)
        * Param         : username of the second user
    """
    return "Match"


@app.route("/pull")
# GET /pull
def pull():
    """
    Pulls the questions and the game state
        * Return        : 200 OK if the game state has been pulled successfully or
        401 Unauthorized (multiple reasons)
        * Param         : -
    """
    return "Pull"


@app.route("/push")
# POST /push
def push():
    """
    Pushes the answers to the server
        * Return        : 200 OK if the answers have been pushed successfully or
        401 Unauthorized (multiple reasons)
        * Param         : answers
    """
    return "Push"


@app.route("/healthcheck")
def healthcheck():
    """
    Checks the health of the server
        * Return        : 200 OK if the server is healthy or other if the server is not healthy
        * Param         : -
    """
    # Try to contact the databases (game and user)

    return "OK"
