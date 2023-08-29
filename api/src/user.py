"""
    * File name     : user.py
    * Utility       : This file contains the user API, which is responsible for the user management
    * Version       : 1.0
    * Creation Date : 07/08/2023
"""
import os
import logging
import random
import mysql.connector as mysql
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from Database.connect import connect_db
from Misc.json_maker import return_json
from Misc.user_logic import (
    is_user_in_db,
    email_to_user_id,
    set_game_state,
    get_db_password,
    create_hashed_password,
    check_password,
)


def open_session():
    """
    * Function      : open_session()
    * Description   : Opens a session for a user with the JWT secret key.
    * Return        : Json with the token and the refresh token
    * Param         : None
    """
    if not request.is_json:
        logging.error("/openSession: no data passed to login fonction")
        return return_json(404, "no data passed to login fonction")

    try:
        _json = request.json
        if not isinstance(_json, dict):
            logging.error("/openSession: json is not dictionnary format")
            return return_json(404, "json is not dictionnary format")

        name = _json.get("name", None)
        password = _json.get("password", None)
        valid_password = False
        if not "front" == name or "dash" == name:
            return return_json(404, "Wrong username")

        if os.getenv("FRONT_TOKEN") == password:
            valid_password = True

        if valid_password:
            token = create_access_token(identity=name)
            refresh_token = create_refresh_token(identity=name)
            return return_json(200, {"token": token, "refresh_token": refresh_token})

        logging.error("/openSession: Passwords mismatch")
    except Exception as err:
        log = "/openSession: json parsing error data -> %s \n %s", str(
            request.args), err
        logging.error(log)
        return return_json(404, log)
    return return_json(404, "Passwords mismatch")

# POST /register


@jwt_required()
def register():
    """
    Register users in the database.

    This function registers users by performing the following checks:
    - Check if the email is not already in the database.
    - Check if the email exists via an SMTP call to z.imt.fr.
    If both checks pass, the user is added to the database.

    This function uses the MySQL connector and Flask request (POST) to get data.
    """
    jwt_identity = get_jwt_identity()
    if jwt_identity != "front":
        return return_json(404, "Unauthorized")

    if not request.is_json:
        logging.error("/register: no data passed to login fonction")
        return return_json(404, "no data passed to login fonction")

    try:
        _json = request.json
    except Exception as err:
        logging.error("/register: json parsing error data -> %s",
                      str(request.args))
        raise err
    if not isinstance(_json, dict):
        logging.error("/register: json is not dictionnary format")
        return return_json(404, "json is not dictionnary format")

    email = _json.get("email", None)
    password = _json.get("password", None)

    # Check if the email exists in LDAP
    # if not is_user_in_db(email, "email", "Ldap"):
    #     return return_json(404, "L'email n'existe pas.")

    # Check if the user is already registered
    if is_user_in_db(email, "email", "Users"):
        return return_json(404, "Cet utilisateur existe déjà.")
    # Generate a random 3-digit ID
    user_id = random.randint(100, 999)
    score = 0
    try:
        cnx = connect_db()
        if cnx is None:
            return return_json(404, "Cannot connect to DB")
        cursor = cnx.cursor()
        # Insert user data into the database
        cursor.execute(
            "INSERT INTO Users (email, password, score, user_id) VALUES (%s, %s, %s, %s)",
            (email, create_hashed_password(password), score, user_id),
        )
        cnx.commit()
    except mysql.Error as err:
        logging.error(
            "Error while inserting user data into the database : %s", err)
        return return_json(404, "Error while inserting user data into the database : ")
    cursor.close()
    cnx.close()
    return return_json(200, "Vous pouvez désormais vous connecter.")


# POST /login
@jwt_required()
def login():
    """
    Logs the user in
        * Return        : 200 OK if the user has been logged in successfully or
        404 Not Found if the user is not registered
        * Param         : username, password
    """
    jwt_identity = get_jwt_identity()
    if jwt_identity != "front":
        return return_json(404, "Unauthorized")

    if not request.is_json:
        logging.error("/login: no data passed to login function")
        return return_json(404, "no data passed to login function")

    try:
        _json = request.json
    except Exception:
        logging.error("/login: json parsing error data -> %s",
                      str(request.args))
        return return_json(404, ("json parsing error data -> " + str(request.args)))
    if not isinstance(_json, dict):
        logging.error("/login: json is not dictionary format")
        return return_json(404, "json is not dictionary format")

    email = _json.get("email", None)
    password = _json.get("password", None)

    if email is None or password is None:
        return return_json(404, "Email ou mot de passe manquant.")

    hashed_db_password = get_db_password(email)
    if hashed_db_password is None:
        return return_json(404, "Vous n'êtes pas inscrit.")
    valid_password = check_password(password, hashed_db_password)

    if valid_password:
        user_id = email_to_user_id(email)
        token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        set_game_state(user_id, 0)
        return return_json(200, {"token": token, "refresh_token": refresh_token, "user_id": user_id})

    logging.error("/login: Passwords mismatch")
    return return_json(404, "Mot de passe incorrect.")
