import logging
import mysql.connector.errors as mysql_errors
from Database.connect import connect_db
from Misc.json_maker import return_json
from Misc.user_logic import get_user_full_name


def dashboard():
    """
    Pulls the ten hightest score and the game state
        * Return        : 200 OK if the game state has been pulled successfully or
        404 Not Found (multiple reasons)
        * Param         : -
    """
    try:
        cnx = connect_db()
        if cnx is None:
            logging.warning("!!!! DASHBOARD Cannot connect to DB !!!!")
            return return_json(404, "Cannot connect to DB")
        cursor = cnx.cursor()
        cursor.execute("SELECT user_id, score FROM Users ORDER BY score DESC")
        result = {}
        cpt = 1
        for item in cursor:
            user_name = get_user_full_name(
                item[0])[0] + " " + get_user_full_name(item[0])[1]
            result[user_name] = item[1]
            cpt = cpt + 1
            if cpt == 11:
                break
        return return_json(200, sorted(result.items(), key=lambda x: x[1], reverse=True))
    except mysql_errors.Error as err:
        logging.error(
            "Error while getting user data from the database : %s", err)
        return return_json(404, "Error while getting user data from the database")
