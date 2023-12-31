"""
    * File name     : app.py
    * Utility       : Entry Point of the api for the game
    * Version       : 1.0
    * Creation Date : 07/08/2023
"""

import logging
import os
import argparse
import time
from sys import stdout
from datetime import timedelta, datetime
from itertools import starmap
from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask, request, make_response
from flask_jwt_extended import JWTManager


# From src
from user import (
    register,
    login,
    open_session,
)
from game import (
    match,
    pull,
    push,
)
from dashboard import dashboard
from Misc.healthcheck import healthcheck
from Misc.json_maker import return_json
from Database.connect import connect_db
from Database.functions import (
    create_db,
    delete_data,
    reset_db,
    load_db,
    load_fake_users
)

load_dotenv()


STR_NOW = datetime.now().strftime("%Y-%m-%d")
FORMAT = "[%(asctime)-15s] - %(levelname)s - %(message)s"

# Creating log folder
LOGS_EXISTS = os.path.exists("logs")
if not LOGS_EXISTS:
    os.makedirs("logs")

LOGS_FOLDER = os.path.join(os.path.dirname(__file__), "logs")
DAILY_LOG = os.path.join(LOGS_FOLDER, f"api_log-{STR_NOW}.log")
fileHandler = logging.FileHandler(filename=os.path.abspath(DAILY_LOG))
streamHandler = logging.StreamHandler(stream=stdout)
handlers = [
    fileHandler,
    streamHandler,
]
logging.basicConfig(format=FORMAT, level=10, handlers=handlers, force=True)

parser = argparse.ArgumentParser()
parser.add_argument("--create-db", action="store_true")
parser.add_argument("--clear-db", action="store_true")
parser.add_argument("--reset-db", action="store_true")
parser.add_argument("--load-db", action="store_true")
parser.add_argument("--load-fake-users", action="store_true")
parser.add_argument("--init", action="store_true")


app: Flask = Flask(__name__)
cors = CORS(app)

# Setup the Flask-JWT-Extended extension
# default algorithm: HS256
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=6)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=90)
jwt = JWTManager(app)


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


@app.before_request
def before_req():
    """
    Check authorization and log data
        * Return        : If not authorized return None to return_json, else pass
        * Param         : None
    """

    to_log = "Start of Request - "
    to_log += "Road asked: " + str(request.path)
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if not request:
        logging.error(to_log)
        return after_req(return_json(None))
    logging.info(to_log)


@app.after_request
def after_req(returned_value):
    """
    Log end of request and return data
        * Return        : Return Data
        * Param         :
            - returned_value    : Data return by previous functions
    """

    to_log = "End of Request - "
    to_log += "Status: " + str(returned_value.status)
    if 200 == returned_value.status_code:
        logging.info(to_log)
    else:
        logging.warning(to_log)
    return returned_value


app.add_url_rule("/openSession", "openSession",
                 open_session, methods=["POST", "OPTIONS"])
app.add_url_rule("/register", "refresh", register, methods=["POST", "OPTIONS"])
app.add_url_rule("/login", "login", login, methods=["POST", "OPTIONS"])
app.add_url_rule("/match", "match", match, methods=["POST", "OPTIONS"])
app.add_url_rule("/pull", "pull", pull, methods=["GET", "OPTIONS"])
app.add_url_rule("/push", "push", push, methods=["GET", "OPTIONS"])
app.add_url_rule("/healthcheck", "healthcheck",
                 healthcheck, methods=["GET", "OPTIONS"])
app.add_url_rule("/pub/leaderboard", "dashboard",
                 dashboard, methods=["GET", "OPTIONS"])


def main(*args, debug=False, run=False):
    """
    Main function of the api
        * Return        : None
        * Param         :
            - args          : Arguments of the main function
            - debug         : If the app is in debug mode
            - run           : If the app should run
    """
    # Disable Flask logs
    app.logger.disabled = True
    logger = logging.getLogger("werkzeug")
    logger.disabled = True

    app_args: argparse.Namespace = (
        parser.parse_args(args) if args else parser.parse_args()
    )
    print(" ==> Main Process Arguments", file=stdout)
    print(
        *starmap("\t{0:>12} : {1:<6}".format, app_args._get_kwargs()),
        sep="\n",
        file=stdout,
    )

    cpt, conn = 12, None
    while cpt:
        conn = connect_db()
        if conn is not None:
            conn.close()
            create_db()
            load_db()
            print("== Connection succeed ==", file=stdout)
            logging.info("== Loading database ==")
            load_db()
            if app_args.clear_db:
                logging.info("== Clearing Database ==")
                delete_data()
            if app_args.reset_db:
                logging.info("== Reseting Database ==")
                reset_db()
            if app_args.load_fake_users:
                logging.info("== Loading Users with fake data ==")
                load_fake_users()
            break
        print("== Connection failed ==", file=stdout)
        cpt -= 1
        time.sleep(5)

    return app.run(debug=debug) if run else app
