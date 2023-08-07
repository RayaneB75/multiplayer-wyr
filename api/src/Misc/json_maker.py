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


def return_json(data=None):
    """
    Function name       : return_json
        * Description   : Return JSON with data
        * Return        : JSON proper response
        * Param         : data to return
    """
    # Send response in function of the result
    if data is not None:
        response = app.response_class(
            response=json.dumps(data), status=200, mimetype="application/json"
        )
    else:
        response = app.response_class(
            response=json.dumps(
                "A problem has occurred, "
                "please try again later or contact administrator."
            ),
            status=503,
            mimetype="application/json",
        )

    # Return response created before
    return response
