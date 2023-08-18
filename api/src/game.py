"""
    * File name     : game.py
    * Utility       : This file contains the game API, which is responsible for the game management
    * Version       : 1.0
    * Creation Date : 07/08/2023
"""

import logging
import random
import mysql.connector.errors as mysql_errors
from flask import Flask, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from Database.connect import connect_db
from user import is_user_in_db, email_to_user_id, is_user_in_game, set_game_state
from Misc.json_maker import return_json

app = Flask(__name__)


@jwt_required()
# POST /match
def match():
    """
    Start a new game with the given user and the logged in user
        * Return        : 200 OK if the game has been started successfully or
        404 Not Found (multiple reasons)
        * Param         : username of the second user
    """

    user_i_email = get_jwt_identity()
    if not is_user_in_db(user_i_email, "email", "Users"):
        return return_json(404, "Vous n'êtes pas connecté")

    user_i = str(email_to_user_id(user_i_email))

    if not request.is_json:
        logging.error("/match: no data passed to function")
        return return_json(404, "no data passed to function")

    try:
        _json = request.json
        if not isinstance(_json, dict):
            logging.error("/match: json is not dictionnary format")
            return return_json(404, "json is not dictionnary format")
        user_r = str(_json.get("userId", None))

        if user_r == user_i:
            return return_json(404, "Vous ne pouvez pas jouer avec vous même")
        if user_r is None or not is_user_in_db(user_r, "user_id", "Users"):
            return return_json(404, "Cet utilisateur n'existe pas")
        check_i = is_user_in_game(user_i)
        check_r = is_user_in_game(user_r)
        logging.debug("check_i : %s", check_i)
        logging.debug("check_r : %s", check_r)
        if check_i is None or check_r is None:
            return return_json(404, "Un problème est survenu lors de la création de la partie")
        if check_i or check_r:
            return return_json(404, "Vous êtes déjà en partie")
        if not is_user_available(user_i, user_r):
            return return_json(404, "Vous avez déjà joué avec cet utilisateur")
        # All the checks are done, we can add the match to the database
        set_game_state(user_i, 1)
        set_game_state(user_r, 1)
    except Exception as err:
        logging.error(
            ("/match: json parsing error data -> %s \n %s", str(request.args), err))
        return return_json(404, "Un problème est survenu lors de la création de la partie")
    return return_json(200, "Match")


@jwt_required()
# GET /pull
def pull():
    """
    Pulls the questions and the game state
        * Return        : 200 OK if the game state has been pulled successfully or
        404 Not Found (multiple reasons)
        * Param         : -
    """
    user_email = get_jwt_identity()
    if not is_user_in_db(user_email, "email", "Users"):
        return return_json(404, "Vous n'êtes pas connecté")

    question_number = random.randint(0, 389)

    try:
        cnx = connect_db()
        if cnx is None:
            logging.error("Cannot connect to DB")
            return return_json(404, "Cannot connect to DB")
        cursor = cnx.cursor()
        query = "SELECT firstProp, secondProp FROM Game WHERE question_id = '%s'"
        cursor.execute(query, (question_number,))
        if cursor.rowcount == 0:
            logging.error("No question found")
            return return_json(404, "No question found")
        question = cursor.fetchone()
        cursor.close()
        cnx.close()
    except mysql_errors.Error as err:
        logging.error(
            "Error while getting user data from the database : %s", err)
        return return_json(404, "Error while getting user data from the database")
    return return_json(200, {"firstProp": question[0], "secondProp": question[1]})


@jwt_required()
# POST /push
def push():
    """
    Pushes the answers to the server
        * Return        : 200 OK if the answers have been pushed successfully or
        404 Not Found (multiple reasons)
        * Param         : answers
    """
    user_i_email = get_jwt_identity()
    if not is_user_in_db(user_i_email, "email", "Users"):
        return return_json(404, "Vous n'êtes pas connecté")

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
        for each_user in cursor:
            if each_user[0] != user_r:
                return False
        cursor.close()
        cnx.close()
        return True
    except mysql_errors.Error as err:
        logging.error(
            "Error while getting user data from the database : %s", err)
        return None
