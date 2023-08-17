"""
This module contains the healthcheck route
"""

from flask import Flask
from json_maker import return_json
from Database.connect import connect_db

app = Flask(__name__)


@app.route("/healthcheck")
def healthcheck():
    """
    Checks the health of the server
        * Return        : 200 OK if the server is healthy or other if the server is not healthy
        * Param         : -
    """
    # Try to contact the databases (game and user)
    # If it fails, return 500
    # Else, return 200
    cnx = connect_db()
    if cnx is None:
        return ("Cannot connect to DB : ", 500)
    cnx.close()

    return return_json(200, "API and databases are healthy")
