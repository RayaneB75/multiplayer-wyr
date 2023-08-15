"""
    * File name     : database_function.py
    * Utility       : Creation of tables in database
    * Version       : 1.0
    * Creation Date : 07/08/2023
"""
import logging
from psycopg import errors as errorcode
from Database.connect import connect_db


CREATE_TABLE_USERS = """\
CREATE TABLE if not exists Users (
    email varchar(100) NOT NULL,
    password varchar(255) NOT NULL,
    score int NOT NULL,
    user_id serial NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (email) REFERENCES Ldap(email)   
);
"""

CREATE_TABLE_MATCHES = """\
CREATE TABLE if not exists Matches (
    user_i serial NOT NULL,
    user_r serial NOT NULL,
    PRIMARY KEY (user_i, user_r)
);
"""

CREATE_TABLE_GAME = """\
CREATE TABLE if not exists Game (
    question_id serial NOT NULL,
    firstProp varchar(255) NOT NULL,
    secondProp varchar(255) NOT NULL,
    PRIMARY KEY (question_id)
);
"""

CREATE_TABLE_LDAP = """\
CREATE TABLE if not exists Ldap (
    email varchar(255) NOT NULL,
    PRIMARY KEY (email)
);
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
        except errorcode.DuplicateTable:
            msg = "already exists."
        except errorcode.Error as err:
            msg = str(err)
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
        except errorcode.DuplicateTable:
            msg = "already exists."
        except errorcode.Error as err:
            msg = str(err)
        print(tmpl_log.format(name, msg))
    cursor.close()
    cnx.close()
    return "OK"
