"""
This file contains all the functions related to the user
    * File name     : user_logic.py
    * Utility       : This file contains the user API, which is responsible for the user management    
"""
import logging
import bcrypt
import mysql.connector as mysql
import mysql.connector.errors as mysql_errors
from Database.connect import connect_db


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
        cursor.execute("SELECT user_i, user_r FROM Matches")

        for item in cursor:
            logging.debug(item[0] == user_i and item[1] == user_r)
            if item[0] == user_i and item[1] == user_r:
                return False
        cursor.close()
        cnx.close()
        return True
    except mysql_errors.Error as err:
        logging.error(
            "Error while getting user data from the database : %s", err)
        return None


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


def get_user_score(user_id):
    """
    Get the score of user in the database
        * Return        : score of the user
        * Param         : user_id
    """
    try:
        cnx = connect_db()
        if cnx is None:
            logging.error("Cannot connect to DB")
            return None
        cursor = cnx.cursor()
        cursor.execute("SELECT user_id, score FROM Users")
        for item in cursor:
            if item[0] == user_id or str(item[0]) == user_id:
                cnx.close()
                return item[1]
        cnx.close()
        return None
    except mysql.Error as err:
        logging.error("Error while getting user score from DB : %s", err)
        return None


def add_new_duel(user_i, user_r,):
    """
    Add a new duel in the database (table Matches)
        * Return        : -
        * Param         : user_i, user_r
    """
    try:
        cnx = connect_db()
        if cnx is None:
            logging.error("Cannot connect to DB")
        cursor = cnx.cursor()
        query = "INSERT INTO Matches (user_i, user_r) VALUES (%s, %s)"
        cursor.execute(query, (user_i, user_r,))
        cnx.commit()
        cnx.close()
    except mysql.Error as err:
        logging.error(
            "Error while getting user data from the database : %s", err)
