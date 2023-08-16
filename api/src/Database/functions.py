"""
    * File name     : database_function.py
    * Utility       : Creation of tables in database
    * Version       : 1.0
    * Creation Date : 07/08/2023
"""
import logging
import mysql.connector as mysql
from pandas import read_csv
from mysql.connector import errorcode
from Database.connect import connect_db


CREATE_TABLE_USERS = """\
CREATE TABLE if not exists `Users` (
    `email` varchar(100) NOT NULL,
    `password` varchar(255) NOT NULL,
    `score` int NOT NULL,
    `user_id` int NOT NULL,
    PRIMARY KEY (`email`),
    FOREIGN KEY (`email`) REFERENCES Ldap(`email`)   
) ENGINE=InnoDB;
"""

CREATE_TABLE_MATCHES = """\
CREATE TABLE if not exists `Matches` (
    `user_i` int NOT NULL,
    `user_r` int NOT NULL,
    PRIMARY KEY (`user_i`,`user_r`)
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
    "Matches": "DROP TABLE Matches",
    "Game": "DROP TABLE Game",
    "Users": "DROP TABLE Users",
    "Ldap": "DROP TABLE Ldap",
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
        # with open(file="Database/mails.export", mode="r", encoding="utf-8") as ldap_file:
        #     query = "SELECT email FROM Ldap"
        #     if cursor.execute(query) != 0:
        #         logging.debug("DB table already filled")
        #         ldap_file.close()
        #         return True
        #     query = "INSERT INTO Ldap (email) VALUES (%s)"
        #     cursor.executemany(query, [(line.strip(),) for line in ldap_file])
        #     cnx.commit()
        #     ldap_file.close()
        with read_csv(filepath_or_buffer="Database/game.csv") as game_file:
            new_dict = game_file.to_dict()
            query = "SELECT email FROM Game"
            if cursor.execute(query) != 0:
                logging.debug("Game table already filled")
                game_file.close()
            query = "INSERT INTO Game (question_id, first_prop, second_prop) VALUES (%s, %s, %s)"
            cursor.executemany(query, [(value[0], value[1], value[2])
                               for value in new_dict.items()])
            cnx.commit()
            game_file.close()
    except mysql.Error as err:
        logging.error(
            "Error while loading data into the database : %s", err)
        return False
    finally:
        cnx.close()
    return True
