from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http
import json

app = Flask(__name__)
CORS(app)

review_URL = environ.get('review_URL') or "http://localhost:5021/review"
cocktail_URL = environ.get('cocktail_URL') or "http://localhost:5022/cocktail"

@app.route("/search_package")
def search_package():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            cocktail = request.get_json()
            print("\nReceived a search request in JSON:", cocktail)

            # 1. Send package search info {user_input}
            result = processSearchPackage(cocktail)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "search_package.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processSearchPackage(cocktail):
    # 2. Get the drink info
    # Invoke the drink information microservice
    print('\n-----Invoking cocktail microservice-----')
    cocktail_result = invoke_http(cocktail_URL, method='GET', json=cocktail)
    print('cocktail_result:', cocktail_result)

    # 5. Get the review for drink
    # Invoke the review microservice
    print('\n\n-----Invoking review microservice-----')
    review_result = invoke_http(review_URL, json=cocktail_result['cocktail_name'])
    print("review_result:", review_result, '\n')

    # 7. Return created package result
    return {
        "code": 201,
        "data": {
            "cocktail_result": cocktail_result,
            "review_result": review_result
        }
    }

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for search package...")
    app.run(host="0.0.0.0", port=5020, debug=True)