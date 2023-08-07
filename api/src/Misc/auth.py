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
    token_parser = os.getenv("PARSER_TOKEN")
    token_app = os.getenv("FRONT_TOKEN")
    token_ansible = os.getenv("ANSIBLE_TOKEN")
    token_postman = os.getenv("POSTMAN_TOKEN")
    token_cron = os.getenv("CRON_TOKEN")
    token_len = 72
    prefix = "Bearer "
    info = "Token_used : "

    # Retrieve token form http_response and return response
    if "Authorization" in http_request.headers:
        bearer = str(http_request.headers["Authorization"])
        if bearer.startswith(prefix) and len(bearer) == (len(prefix) + token_len):
            bearer = bearer[len(prefix) :]
            if bearer == token_app:
                info += "app"
                logging.info(info)
                return "app"
            elif bearer == token_ansible:
                info += "ansible"
                logging.info(info)
                return "ansible"
            elif bearer == token_parser:
                info += "parser"
                logging.info(info)
                return "parser"
            elif bearer == token_postman:
                info += "postman"
                logging.info(info)
                return "postman"
            elif bearer == token_cron:
                info += "cron"
                logging.info(info)
                return "cron"
            else:
                info += "unknown : " + bearer
                logging.info(info)
                return None
        else:
            msg = "Authorization: bearer prefix not valid"
            logging.warning(msg)
            return None
    else:
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
    list_app = [["/company/name", "GET"], ["/blog", "GET"]]
    list_ansible = [["/company", "GET"], ["/company", "POST"], ["/company", "DELETE"]]
    list_parser = [["/company/name", "GET"], ["/company/email", "GET"]]
    list_postman = [
        ["/company", "GET"],
        ["/company/name", "GET"],
        ["/company/email", "GET"],
        ["/company", "POST"],
        ["/company", "UPDATE"],
        ["/company", "DELETE"],
        ["/blog", "GET"],
        ["/blog", "POST"],
        ["/blog", "UPDATE"],
        ["/blog", "DELETE"],
    ]
    list_cron = [["/blog", "GET"], ["/blog/update", "GET"]]

    # Get token name
    token_used = check_token(http_request)

    # Check if users is authorised by checking the path & method couple in lists
    if token_used is not None:
        path = http_request.path
        if path[0:5] == "/blog":
            path_to_use = path[0:5]
        elif path[0:8] == "/company" and http_request.method != "GET":
            path_to_use = path[0:8]
        elif path[0:8] == "/company" and http_request.method == "GET":
            if len(path) == 8:
                path_to_use = path
            elif path[0:13] == "/company/name":
                path_to_use = path[0:13]
            elif path[0:14] == "/company/email":
                path_to_use = path[0:14]
            else:
                path_to_use = None
        else:
            path_to_use = None

        list_to_test = [path_to_use, http_request.method]

        if token_used == "app" and list_to_test in list_app:
            return True
        elif token_used == "ansible" and list_to_test in list_ansible:
            return True
        elif token_used == "parser" and list_to_test in list_parser:
            return True
        elif token_used == "postman" and list_to_test in list_postman:
            return True
        elif token_used == "cron" and list_to_test in list_cron:
            return True
        else:
            return False
    else:
        return False
