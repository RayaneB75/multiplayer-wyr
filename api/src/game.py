import logging
import mysql.connector.errors as mysql_errors
from Database.connect import connect_db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, request
from user import is_user_in_db, email_to_user_id
from Misc.json_maker import return_json

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
    
    user_i_email = get_jwt_identity()
    user_i = email_to_user_id(user_i_email)
    if not request.is_json:
        logging.error("/match: no data passed to function")
        return return_json()
    
    try:
        _json = request.json
    except Exception as err:
        logging.error("/match: json parsing error data -> " + str(request.args))
        return (return_json(f"/openSession: json parsing error data -> {str(request.args)}"))
    if not isinstance(_json, dict):
        logging.error("/match: json is not dictionnary format")
        return return_json("json is not dictionnary format")
    user_r = _json.get("userId", None)
    if user_r is None:
        return return_json("userId is not in json")
    if not is_user_in_db(user_r, "user_id"):
        return return_json("User doesn't exist in database")
    if not is_user_available(user_i, user_r):
        return return_json("User is not available")
    
    return return_json("Match")

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

def is_user_available(user_i, user_r):
    """
    Check if the user is available to play
        * Return        : True if the user is available, False otherwise
        * Param         : user
    """
    try:
        cnx = connect_db()
        if cnx is None:
            logging.error("Cannot connect to DB")
            return None
        cursor = cnx.cursor()
        query = "SELECT user_r FROM Matches WHERE user_i = %s"
        cursor.execute(query, (user_i,))
        if cursor.rowcount == 0:
            return True
        for (user_r) in cursor:
            if user_r[0] != user_r:
                return False
        cursor.close()
        cnx.close()
        return True
    except mysql_errors.Error as err:
        logging.error("Error while getting user data from the database : %s", err)
        return None