"""
    * File name     : database_function.py
    * Utility       : Creation of tables in database
    * Version       : 1.0
    * Creation Date : 07/08/2023
"""
import logging
import mysql.connector
from mysql.connector import errorcode
from src.Database.connect import connect_db


CREATE_TABLE_USERS = """\
CREATE TABLE if not exists `Users` (
    `email` varchar(40) NOT NULL UNIQUE,
    `password` varchar(255) NOT NULL,
    `score` int(11),
    PRIMARY KEY (`email`)
) ENGINE=InnoDB
"""

CREATE_TABLE_GAME = """\
CREATE TABLE if not exists `Game` (
    `question_id` int(11) NOT NULL AUTO_INCREMENT,
    `firstProp` varchar(255) NOT NULL,
    `secondProp` varchar(255) NOT NULL,
    PRIMARY KEY (`question_id`)
) ENGINE=InnoDB
"""

create_tables = {
    "Users": CREATE_TABLE_USERS,
    "Game": CREATE_TABLE_GAME,
}

delete_tables = {
    "Users": "DELETE FROM Users",
    "Game": "DELETE FROM Game",
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
        return "503: Un problème est survenu, veuillez réessayer plus tard"

    cursor = cnx.cursor()
    tmpl_log = "Creating table {0:>10} : {1:<20}"
    for name, description in create_tables.items():
        msg = "OK"
        try:
            cursor.execute(description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                msg = "already exists."
            else:
                msg = err.msg
        print(tmpl_log.format(name, msg))
    cursor.close()
    cnx.close()


def delete_data(connection=None):
    """
    This function delete all data in database
        * Return        : Nothing
        * Param         : "Connection" as None
    """
    cnx = connect_db() if connection is None else connection
    if cnx is None:
        return "503: Un problème est survenu, veuillez réessayer plus tard"

    cursor = cnx.cursor()
    for query in delete_tables.values():
        cursor.execute(query)
    cnx.commit()
    cursor.close()

    cnx.close()
