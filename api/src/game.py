"""
    * File name     : game.py
    * Utility       : This file contains the game API, which is responsible for the game management
    * Version       : 1.0
    * Creation Date : 07/08/2023
"""

import logging
import random
import mysql.connector.errors as mysql_errors
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from Database.connect import connect_db
from Misc.user_logic import (
    is_user_in_db,
    email_to_user_id,
    set_game_state,
    is_user_in_game,
    is_duo_available,
    get_user_score,
    add_new_duel,
    get_user_full_name
)
from Misc.json_maker import return_json


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

    if not request.is_json or not isinstance(request.json, dict):
        logging.error("/match: no or wrong data passed to function")
        return return_json(404, "no or wrong data passed to function")

    try:
        _json = request.json
        user_r = str(_json.get("userId", None))

        if user_r == user_i:
            return return_json(404, "Vous ne pouvez pas jouer avec vous même")
        if user_r is None or not is_user_in_db(user_r, "user_id", "Users"):
            return return_json(404, "Cet utilisateur n'existe pas")
        if is_user_in_game(user_r) != 0:
            return return_json(404, "Le joueur est déjà en partie")
        if not is_duo_available(user_i, user_r):
            return return_json(404, "Vous avez déjà joué avec cet utilisateur")
        # All the checks are done, we can add the match to the database
        set_game_state(user_i, user_r)
        set_game_state(user_r, user_i)
    except Exception as err:
        logging.error(
            ("/match: json parsing error data -> %s \n %s", str(request.args), err))
        return return_json(404, "Un problème est survenu lors de la création de la partie")
    user_full_name = get_user_full_name(user_r)
    result = user_full_name[0] + " " + user_full_name[1]
    return return_json(200, {"dueled_user": result})


@jwt_required()
# GET /pull
def pull():
    """
    Pulls the questions and the game state
        * Return        : 200 OK if the game state has been pulled successfully or
        404 Not Found (multiple reasons)
        * Param         : -
    """
    user_i_email = get_jwt_identity()
    if not is_user_in_db(user_i_email, "email", "Users"):
        return return_json(404, "Vous n'êtes pas connecté")

    if is_user_in_game(email_to_user_id(user_i_email)) == 0:
        return return_json(404, "Vous n'avez pas de partie en cours")

    question_number = random.randint(1, 389)

    try:
        cnx = connect_db()
        if cnx is None:
            logging.error("Cannot connect to DB")
            return return_json(404, "Cannot connect to DB")
        cursor = cnx.cursor()
        cursor.execute("SELECT question_id, first_prop, second_prop FROM Game")
        for item in cursor:
            if item[0] == question_number or str(item[0]) == question_number:
                cnx.close()
                return return_json(200, {"first_prop": item[1], "second_prop": item[2]})
        return None
    except mysql_errors.Error as err:
        logging.error(
            "Error while getting user data from the database : %s", err)
        return return_json(404, "Error while getting user data from the database")


@jwt_required()
# GET /push
def push():
    """
    Pushes the answers to the server
        * Return        : 200 OK if the answers have been pushed successfully or
        404 Not Found (multiple reasons)
        * Param         : user_id of the user who answered
    """
    user_i_email = get_jwt_identity()
    user_i = email_to_user_id(user_i_email)
    if not is_user_in_db(user_i_email, "email", "Users"):
        return return_json(404, "Vous n'êtes pas connecté")

    if is_user_in_game(email_to_user_id(user_i_email)) == 0:
        return return_json(404, "Vous n'avez pas de partie en cours")

    try:
        user_r = is_user_in_game(user_i)
        cnx = connect_db()
        if cnx is None:
            logging.error("Cannot connect to DB")
            return return_json(404, "Cannot connect to DB")

        cursor = cnx.cursor()
        new_score_i = 0
        new_score = 0
        for user in [user_i, user_r]:
            if user == user_i:
                new_score = get_user_score(user) + 3
                new_score_i = new_score
            if user == user_r:
                new_score = get_user_score(user) + 1
            logging.debug("nouvau score pour %s : %s", user, new_score)
            cursor.execute(
                "UPDATE Users SET score = %s WHERE user_id = %s", (new_score, user,))
        cnx.commit()
        set_game_state(user_i, 0)
        set_game_state(user_r, 0)
        add_new_duel(user_i, user_r)

    except Exception as err:
        logging.error(
            ("/push: json parsing error data -> %s \n %s", str(request.args), err))
        return return_json(404, "Un problème est survenu lors de la création de la partie")
    result = "Nouveau score : " + str(new_score_i)
    return return_json(200, result)
