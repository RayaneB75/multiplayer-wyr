"""
    * File name     : connect.py
    * Utility       : Connection to Database
    * Version       : 1.0
    * Creation Date : 07/08/2023
    * Imports       :
        - mysql_properties : Properties of the database
        - psycopg library
"""
import os
import logging
import psycopg as psql


config = {
    "dbname": os.getenv("POSTGRES_DB", "app_inte"),
    "user": os.getenv("POSTGRES_USER", "api"),
    "password": os.getenv("POSTGRES_PASSWORD", "api"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}


def connect_db():
    """
    * Function      : Initiate connection to database
    * Return        : cnx connection
    * Param         : None
    """
    cnx = None
    try:
        cnx = psql.connect(**config)
    except psql.Error as err:
        logging.error("Cannot connect to DB")
        print(err)
    return cnx
