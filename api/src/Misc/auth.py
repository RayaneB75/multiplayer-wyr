"""
    Module name     : auth
    Description     : Check if user is authorised
    Version         : 1.0
    Creation date   : 08/07/2023
"""

import os
import logging
from flask import Flask

app = Flask(__name__)


def check_token(http_request):
    """
    Function name       : check_token
        * Description   : Check which token is used
        * Return        : Name of token used or None
        * Param         : http request
    """
    # Token to be used in app
    token_front = os.getenv("FRONT_TOKEN")
    token_dash = os.getenv("DASH_TOKEN")
    token_len = 72
    prefix = "Bearer "

    # Retrieve token form http_response and return response
    if "Authorization" in http_request.headers:
        bearer = str(http_request.headers["Authorization"])
        if bearer.startswith(prefix) and len(bearer) == (len(prefix) + token_len):
            bearer = bearer[len(prefix) :]
            if bearer == token_front:
                logging.info("Front token used")
                return "front"
            if bearer == token_dash:
                logging.info("Dashboard token used")
                return "dashboard"
            return None
        msg = "Authorization: bearer prefix not valid"
        logging.warning(msg)
        return None
    msg = "Authorization: Label not in headers"
    logging.warning(msg)
    return None


def check_authorisation(http_request):
    """
    Function name       : check_authorisation
        * Description   : Check if user is authorised
        * Return        : True or False
        * Param         : http_request
    """
    # List of authorisation by application usage
    list_front = [
        ["/openSession", "POST"],
        ["/register", "POST"],
        ["/login", "POST"],
        ["/match", "POST"],
        ["/pull", "GET"],
        ["/push", "POST"],
    ]
    list_dashboard = [["/display/dashboard", "GET"], ["/display/scoreboard", "GET"]]

    # Get token name
    token_used = check_token(http_request)

    # Check if users is authorised by checking the path & method couple in lists
    if token_used is not None:
        path_to_use = http_request.path

        list_to_test = [path_to_use, http_request.method]

        if token_used == "front" and list_to_test in list_front:
            return True
        if token_used == "dashboard" and list_to_test in list_dashboard:
            return True
        return False
    return False
