"""
    * File name     : connect.py
    * Utility       : Connection to Database
    * Version       : 1.0
    * Creation Date : 07/08/2023
    * Imports       :
        - mysql_properties : Properties of the database
        - mysql.connector library
"""
import os
import logging
import mysql.connector as mysql


config = {
    "database": os.getenv("MYSQL_DATABASE", "app_inte"),
    "user": os.getenv("MYSQL_USER", "api"),
    "password": os.getenv("MYSQL_PASSWORD", "api"),
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": os.getenv("MYSQL_PORT", "3306"),
    "raise_on_warnings": True,
}


def connect_db():
    """
    * Function      : Initiate connection to database
    * Return        : cnx connection
    * Param         : None
    """
    cnx = None
    try:
        cnx = mysql.connect(**config)
    except mysql.Error as err:
        logging.error("Cannot connect to DB")
        print(err)
    return cnx
