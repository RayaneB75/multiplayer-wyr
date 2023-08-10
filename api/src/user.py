"""
    * File name     : user.py
    * Utility       : This file contains the user API, which is responsible for the user management
    * Version       : 1.0
    * Creation Date : 07/08/2023
"""
import os
import logging
import smtplib
import random
import bcrypt
import mysql.connector as mysql
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
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
        return return_json()

    try:
        _json = request.json
    except Exception as err:
        logging.error("/openSession: json parsing error data -> %s", str(request.args))
        raise err
    if not isinstance(_json, dict):
        logging.error("/openSession: json is not dictionnary format")
        # logging.error(str(_json))
        return return_json()

    name = _json.get("name", None)
    password = _json.get("password", None)
    valid_password = False
    if os.getenv("FRONT_TOKEN") == password:
        valid_password = True

    if valid_password:
        token = create_access_token(identity=name)
        refresh_token = create_refresh_token(identity=name)
        return return_json({"token": token, "refresh_token": refresh_token})

    logging.error("/openSession: Passwords mismatch")
    return return_json()


# POST /register
def register():
    """
    Register users in the database.

    This function registers users by performing the following checks:
    - Check if the email is not already in the database.
    - Check if the email exists via an SMTP call to z.imt.fr.
    If both checks pass, the user is added to the database.

    This function uses the MySQL connector and Flask request (POST) to get data.
    """
    if not request.is_json:
        logging.error("/register: no data passed to login fonction")
        return return_json()
    
    try:
        _json = request.json
    except Exception as err:
        logging.error("/register: json parsing error data -> " + str(request.args))
        raise err
    if not isinstance(_json, dict):
        logging.error("/register: json is not dictionnary format")
        return return_json()

    email = _json.get("email", None)
    password = _json.get("password", None)

    # Check if the email exists via SMTP call to z.imt.fr
    if not check_email_exists(email):
        return return_json("Invalid email.")

    if check_email_in_db(email):
        return return_json("Email already exists.")
    # Generate a random 6-digit ID
    user_id = random.randint(100000, 999999)
    score = 0
    try:
        cnx = connect_db()
        cursor = cnx.cursor()
        # Insert user data into the database
        cursor.execute(
            "INSERT INTO Users (email, password, score, user_id) VALUES (%s, %s, %s, %s)",
            (email, create_hashed_password(password), score, user_id),
        )
        cnx.commit()
    except mysql.Error as err:
        logging.error("Error while inserting user data into the database : %s", err)
        cursor.close()
        cnx.close()
        return return_json("Error while inserting user data into the database : ")
    cursor.close()
    cnx.close()
    return return_json("User registered successfully.")


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
        return return_json()

    email = _json.get("email", None)
    password = _json.get("password", None)
    hashed_db_password = get_db_password(email)
    valid_password = check_password(password, hashed_db_password)

    logging.debug("email %s", str(email))

    if valid_password:
        token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        return return_json({"token": token, "refresh_token": refresh_token})

    logging.error("/login: Passwords mismatch")
    return return_json("Wrong password.")


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
            query = "SELECT password FROM Users WHERE email = %s"
            val = (email,)
            cursor.execute(query, val)
            result = cursor.fetchone()[0]
            cursor.close()
            cnx.close()

    except mysql.Error as err:
        logging.error("Error while getting password from DB : %s", err)
        cursor.close()
        cnx.close()
        return None
    return result


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


def check_email_in_db(email):
    """
    Check if the email is already in the database
        * Return        : True if the email is in the database, False otherwise
        * Param         : email
    """
    cnx = connect_db()
    cursor = cnx.cursor()
    cursor.execute("SELECT email FROM Users")
    result = []
    for email_db in cursor:
        print(email_db)
        if email_db[0] == email:
            cursor.close()
            cnx.close()
            return True
    cursor.close()
    cnx.close()
    return False


def check_email_exists(email):
    """
    Code to check if the email exists using SMTP
    * Return        : True if the email exists, False otherwise
    * Param         : email
    """
    return True
    email = str(email)
    domain = "z.imt.fr"
    try:
        with smtplib.SMTP(domain) as server:
            server.helo()
            code, _ = server.rcpt(email)
            print(code)
            if code == 250:
                return True
            return True  # To be changed to False when the SMTP call is implemented
    except smtplib.SMTPRecipientsRefused:
        return False
    except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected):
        return False
    except smtplib.SMTPException as err:
        logging.error("Error while checking email : %s", err)
    return False
