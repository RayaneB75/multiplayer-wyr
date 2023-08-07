"""
    * File name     : user.py
    * Utility       : This file contains the user API, which is responsible for the user management
    * Version       : 1.0
    * Creation Date : 07/08/2023
"""
import logging
import bcrypt
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
from src.Database.connect import connect_db
from src.Misc.json_maker import return_json


# POST /register
def register():
    """
    Registers the user in the database
        * Return        : 200 OK if the user has been registered successfully
        * Param         : username, password, email
    """
    return "Register"


# POST /login
def login():
    """
    Logs the user in
        * Return        : 200 OK if the user has been logged in successfully or
        401 Unauthorized if the user is not registered
        * Param         : username, password
    """

    if not request.is_json:
        logging.error("/login: no data passed to login function")
        return return_json()

    try:
        _json = request.json
    except Exception as err:
        logging.error("/login: json parsing error data -> %s", str(request.args))
        raise err
    if not isinstance(_json, dict):
        logging.error("/login: json is not dictionary format")
        # logging.error(str(_json))
        return return_json()

    email = _json.get("email", None)
    password = _json.get("password", None)
    hashed_password = get_db_password(email)
    valid_password = check_password(password, hashed_password)

    logging.debug("email %s", str(email))

    if valid_password:
        token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        return return_json({"token": token, "refresh_token": refresh_token})

    logging.error("/login: Passwords mismatch")
    return return_json()


def get_db_password(email):
    """
    Get the password of user in the database
        * Return        : Password of the service
        * Param         : name_service
    """
    cnx = connect_db()
    if cnx is None:
        logging.error("Cannot connect to DB")
        return None

    result = None
    if email:
        cursor = cnx.cursor()
        query = "SELECT password FROM Users WHERE email = %s"
        val = (email,)
        cursor.execute(query, val)
        result = cursor.fetchone()[0]
        cursor.close()

    cnx.close()
    return result


def create_hashed_password(plain_text_password):
    """
    Hash a password for the first time
    (Using bcrypt, the salt is saved into the hash itself)
    """
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    """
    Check hashed password. Using bcrypt, the salt is saved into the hash itself
    """
    if hashed_password is None:
        return False
    if not isinstance(hashed_password, str):
        raise Exception
    return bcrypt.checkpw(plain_text_password, hashed_password)
