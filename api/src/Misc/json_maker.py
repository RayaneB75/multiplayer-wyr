"""
    * File name     : other_functions.py
    * Utility       : Misc functions for other classes
    * Version       : 3.0
    * Creation Date : 22/02/2021
    * Imports       :
        - logging library
        - os library
        - Flask and json from Flask library
"""


from flask import Flask, json

app = Flask(__name__)


def return_json(code, data=None):
    """
    Function name       : return_json
        * Description   : Return JSON with data
        * Return        : JSON proper response
        * Param         : data to return
    """
    # Send response in function of the result
    if data is not None:
        response = app.response_class(
            response=json.dumps(data), status=code, mimetype="application/json"
        )
    else:
        response = app.response_class(
            response=json.dumps(
                "A problem has occurred, "
                "please try again later or contact administrator."
            ),
            status=code,
            mimetype="application/json",
        )

    # Return response created before
    return response


def is_json(myjson):
    """ Checks if the given string is a json

    Args:
        myjson (string): string to check

    Returns:
        bool: True if the string is a json, False otherwise
    """
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True
