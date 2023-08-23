"""
    * File name     : database_function.py
    * Utility       : Creation of tables in database
    * Version       : 1.0
    * Creation Date : 07/08/2023
"""
import logging
import json
import random
import mysql.connector as mysql
from mysql.connector import errorcode
from user import create_hashed_password
from Database.connect import connect_db


CREATE_TABLE_USERS = """\
CREATE TABLE if not exists `Users` (
    `email` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    `score` int NOT NULL,
    `user_id` int NOT NULL,
    `in_game_with` int NOT NULL DEFAULT "0" CHECK(in_game_with IN ("0", "999999")),
    PRIMARY KEY (`user_id`),
    FOREIGN KEY (`email`) REFERENCES Ldap(`email`)
) ENGINE=InnoDB;
"""

CREATE_TABLE_MATCHES = """\
CREATE TABLE if not exists `Matches` (
    `user_i` int NOT NULL,
    `user_r` int NOT NULL,
    PRIMARY KEY (`user_i`,`user_r`),
    FOREIGN KEY (`user_i`) REFERENCES Users(`user_id`),
    FOREIGN KEY (`user_r`) REFERENCES Users(`user_id`)
) ENGINE=InnoDB;
"""

CREATE_TABLE_GAME = """\
CREATE TABLE if not exists `Game` (
    `question_id` int NOT NULL AUTO_INCREMENT,
    `first_prop` varchar(255) NOT NULL,
    `second_prop` varchar(255) NOT NULL,
    PRIMARY KEY (`question_id`)
) ENGINE=InnoDB;
"""

CREATE_TABLE_LDAP = """\
CREATE TABLE if not exists `Ldap` (
    `email` varchar(255) NOT NULL,
    PRIMARY KEY (`email`)
) ENGINE=InnoDB;
"""


create_tables = {
    "Ldap": CREATE_TABLE_LDAP,
    "Users": CREATE_TABLE_USERS,
    "Game": CREATE_TABLE_GAME,
    "Matches": CREATE_TABLE_MATCHES,
}

delete_tables = {
    "Matches": "DELETE FROM Matches",
    "Game": "DELETE FROM Game",
    "Users": "DELETE FROM Users",
    "Ldap": "DELETE FROM Ldap",
}

drop_tables = {
    "Matches": "DROP TABLE IF EXISTS Matches",
    "Game": "DROP TABLE IF EXISTS Game",
    "Users": "DROP TABLE IF EXISTS Users",
    "Ldap": "DROP TABLE IF EXISTS Ldap",
}


def create_db():
    """
    Function name       : create_db()
        * Function      : Create Table of database if not created
        * Return        : Nothing
        * Param         : None
    """
    cnx = connect_db()
    if cnx is None:
        logging.error("db connection failed")
        return "404: Un problème est survenu, veuillez réessayer plus tard"

    cursor = cnx.cursor()
    tmpl_log = "Creating table {0:>10} : {1:<20}"
    for name, description in create_tables.items():
        msg = "OK"
        try:
            cursor.execute(description)
        except mysql.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                msg = "already exists."
            else:
                msg = err.msg
        print(tmpl_log.format(name, msg))
    cursor.close()
    cnx.close()
    return "OK"


def delete_data(connection=None):
    """
    This function delete all data in database
        * Return        : Nothing
        * Param         : "Connection" as None
    """
    cnx = connect_db() if connection is None else connection
    if cnx is None:
        return "404: Un problème est survenu, veuillez réessayer plus tard"

    cursor = cnx.cursor()
    for query in delete_tables.values():
        cursor.execute(query)
    cnx.commit()
    cursor.close()

    cnx.close()
    return "OK"


def reset_db():
    """
    Function name       : create_db()
        * Function      : Create Table of database if not created
        * Return        : Nothing
        * Param         : None
    """
    cnx = connect_db()
    if cnx is None:
        logging.error("db connection failed")
        return "404: Un problème est survenu, veuillez réessayer plus tard"

    cursor = cnx.cursor()
    tmpl_log = "Creating table {0:>10} : {1:<20}"

    for query in drop_tables.values():
        cursor.execute(query)

    for name, description in create_tables.items():
        msg = "OK"
        try:
            cursor.execute(description)
        except mysql.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                msg = "already exists."
            else:
                msg = err.msg
        print(tmpl_log.format(name, msg))
    cursor.close()
    cnx.close()
    return "OK"


def load_db():
    """
    Function name       : load_db()
        * Function      : Load data into Ldap and Game tables
        * Return        : Boolean 
        * Param         : None
    """
    try:
        cnx = connect_db()
        cursor = cnx.cursor()
        if cnx is None:
            logging.error("db connection failed")
            return False
        with open(file="Database/mails.export", mode="r", encoding="utf-8") as ldap_file:
            cursor.execute("SELECT COUNT(*) FROM Ldap")
            row_count = cursor.fetchone()[0]
            if row_count == 0:
                query = "INSERT INTO Ldap (email) VALUES (%s)"
                cursor.executemany(query, [(line.strip(),)
                                   for line in ldap_file])
                cnx.commit()
            else:
                logging.info("Ldap table already filled")
            ldap_file.close()
        with open(file="Database/game_set/wyr_fr.json", mode="r", encoding="utf-8") as game_file:
            new_dict = json.load(game_file)
            cursor.execute("SELECT COUNT(*) FROM Game")
            row_count = cursor.fetchone()[0]
            if row_count == 0:
                for idx, item in enumerate(new_dict, start=1):
                    first_prop, second_prop = item
                    cursor.execute('''
                        INSERT INTO Game (question_id, first_prop, second_prop)
                        VALUES (%s, %s, %s)
                    ''', (idx, first_prop, second_prop))
                cnx.commit()
            else:
                logging.info("Game table already filled")
            game_file.close()
    except mysql.Error as err:
        logging.error(
            "Error while loading data into the database : %s", err)
        return False
    finally:
        cnx.close()
    return True


def load_fake_users():
    """
    Function name       : load_fake_users()
        * Function      : Load fake users into Users
        * Return        : Boolean
        * Param         : None
    """
    try:
        cnx = connect_db()
        cursor = cnx.cursor()
        if cnx is None:
            logging.error("db connection failed")
            return False
        with open(file="Database/fake_users.json", mode="r", encoding="utf-8") as fake_file:
            new_dict = json.load(fake_file)
            cursor.execute("SELECT COUNT(*) FROM Users")
            row_count = cursor.fetchone()[0]
            if row_count == 0:
                for item in new_dict:
                    email, password = item
                    password = create_hashed_password(password)
                    user_id = random.randint(100000, 999999)
                    score = random.randint(0, 100)
                    query = '''
                        INSERT INTO Users (email, password, score, user_id)
                        VALUES (%s, %s, %s, %s)
                        '''
                    val = (email, password, score, user_id)
                    # Insert user data into the database
                    cursor.execute(query, val)
                cnx.commit()
            else:
                logging.info("Users table already filled")
            fake_file.close()
    except mysql.Error as err:
        logging.error(
            "Error while loading data into the database : %s", err)
        return False
    finally:
        cnx.close()
    return True
