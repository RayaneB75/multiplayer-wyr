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
import mysql.connector


config = {
    "database": os.getenv("MYSQL_DATABASE", "inte"),
    "user": os.getenv("MYSQL_USER", "api"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "host": os.getenv("MYSQL_HOST"),
    "port": os.getenv("MYSQL_PORT", "3306"),
    "raise_on_warnings": True,
}


def connect_db():
    """
    * Function      : Initiate connection to database
    * Return        : cnx connection
    * Param         : None
    """
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        logging.error("Cannot connect to DB")
        print(err)
    return cnx
