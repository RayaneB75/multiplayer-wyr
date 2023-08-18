"""
    * File name     : user.py
    * Utility       : This file contains the user API, which is responsible for the user management
    * Version       : 1.0
    * Creation Date : 07/08/2023
"""
import os
import logging
import random
import bcrypt
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
    if not is_user_in_db(email, "email", "Ldap"):
        return return_json(404, "Invalid email.")

    # Check if the user is already registered
    if is_user_in_db(email, "email", "Users"):
        return return_json(404, "Email already exists.")
    # Generate a random 6-digit ID
    user_id = random.randint(100000, 999999)
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
    return return_json(200, "User registered successfully.")


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
    logging.info("%s trying to connnect", email)

    if email is None or password is None:
        return return_json(404, "Missing email or password.")

    hashed_db_password = get_db_password(email)
    if hashed_db_password is None:
        return return_json(404, "User not registered.")
    valid_password = check_password(password, hashed_db_password)

    if valid_password:
        user_id = email_to_user_id(email)
        token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        set_game_state(user_id, 0)
        return return_json(200, {"token": token, "refresh_token": refresh_token, "user_id": user_id})

    logging.error("/login: Passwords mismatch")
    return return_json(404, "Wrong password.")


def get_db_password(email):
    """
    Get the password of user in the database
        * Return        : Password of the service
        * Param         : name_service
    """
    try:
        cnx = connect_db()
        if cnx is None:
            logging.error("Cannot connect to DB")
            return None

        result = None
        if email:
            cursor = cnx.cursor()
            cursor.execute("SELECT email, password FROM Users")
            for item in cursor:
                if item[0] == email or str(item[0]) == email:
                    result = item[1]
                    cnx.close()
                    return result
        cnx.close()
        return None
    except mysql.Error as err:
        logging.error("Error while getting password from DB : %s", err)
        return None


def create_hashed_password(plain_text_password):
    """
    Hash a password for the first time
    (Using bcrypt, the salt is saved into the hash itself)
    * Return        : Hashed password
    * Param         : plain_text_password
    """
    return bcrypt.hashpw(plain_text_password.encode("utf-8"), bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    """
    Check hashed password. Using bcrypt, the salt is saved into the hash itself
    * Return        : True if the password is correct, False otherwise
    * Param         : plain_text_password, hashed_password
    """
    if hashed_password is None:
        return False
    if not isinstance(hashed_password, str):
        raise TypeError("hashed_password must be a string")
    return bcrypt.checkpw(plain_text_password.encode("utf-8"), hashed_password.encode("utf-8"))


def is_user_in_db(iden, id_type, table):
    """
    Check if the email is already in the database
        * Return        : True if the email is in the database, False otherwise
        * Param         : email
    """
    try:
        cnx = connect_db()
        if cnx is None:
            logging.error("Cannot connect to DB")
            return False
        cursor = cnx.cursor()
        if table == "Users":
            if id_type == "email":
                cursor.execute("SELECT email FROM Users")
            elif id_type == "user_id":
                cursor.execute("SELECT user_id FROM Users")
        else:
            cursor.execute("SELECT email FROM Ldap")

        for item in cursor:
            if item[0] == iden or str(item[0]) == iden:
                cnx.close()
                return True
        cursor.close()
        cnx.close()
        return False
    except mysql.Error as err:
        logging.error("Error while checking if user is in DB : %s", err)
        return False


def is_user_in_game(user_id) -> bool:
    """	
    Check if the user is in game
        * Return        : True if the user is in game, False otherwise
        * Param         : user_id
    """
    try:
        cnx = connect_db()
        result = False
        if cnx is None:
            logging.error("Cannot connect to DB")
            return None
        cursor = cnx.cursor()
        cursor.execute("SELECT user_id, in_game FROM Users")
        for item in cursor:
            if item[0] == user_id or str(item[0]) == user_id:
                if item[1] == '1':
                    result = True
                cnx.close()
                return result
        cnx.close()
        return result
    except mysql.Error as err:
        logging.error("Error while checking if user is in game : %s", err)
        return None


def email_to_user_id(email):
    """
    Get the user_id of user in the database
        * Return        : user_id of the user
        * Param         : email
    """
    try:
        cnx = connect_db()
        if cnx is None:
            logging.error("Cannot connect to DB")
            return None

        result = None
        cursor = cnx.cursor()
        cursor.execute("SELECT email, user_id FROM Users")
        for item in cursor:
            if item[0] == email or str(item[0]) == email:
                result = item[1]
                cnx.close()
                return result
        cnx.close()
        return result
    except mysql.Error as err:
        logging.error("Error while getting user_id from DB : %s", err)
        return None


def set_game_state(user_id, state):
    """
    Changing user's game state in the database
        * Return        : -
        * Param         : user id and user's new game state
    """
    try:
        cnx = connect_db()
        if cnx is None:
            logging.error("Cannot connect to DB")
        cursor = cnx.cursor()
        query = "UPDATE Users SET in_game = %s WHERE user_id = %s"
        cursor.execute(query, (state, user_id,))

        cnx.commit()
        cnx.close()
    except mysql.Error as err:
        logging.error(
            "Error while getting user data from the database : %s", err)
