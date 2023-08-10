import mysql.connector.errors as mysql_errors
from Database.connect import connect_db
from flask_jwt_extended import jwt_required
from flask import Flask

app = Flask(__name__)


@jwt_required()
# POST /match
def match():
    """
    Start a new game with the given user and the logged in user
        * Return        : 200 OK if the game has been started successfully or
        401 Unauthorized (multiple reasons)
        * Param         : username of the second user
    """
    return "Match"


@jwt_required()
# GET /pull
def pull():
    """
    Pulls the questions and the game state
        * Return        : 200 OK if the game state has been pulled successfully or
        401 Unauthorized (multiple reasons)
        * Param         : -
    """
    return "Pull"


@jwt_required()
# POST /push
def push():
    """
    Pushes the answers to the server
        * Return        : 200 OK if the answers have been pushed successfully or
        401 Unauthorized (multiple reasons)
        * Param         : answers
    """
    return "Push"
