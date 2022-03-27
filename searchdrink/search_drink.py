from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

review_URL = "http://localhost:5021/review"
drinkinfo_URL = "http://localhost:5022/drink_information"

@app.route("/search_drink")
def search_drink():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            drink = request.get_json()
            print("\nReceived an order in JSON:", drink)

            # do the actual work
            # 1. Send order info {cart items}
            result = processSearchDrink(drink)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "search_drink.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processSearchDrink(drink):
    # 2. Get the drink info
    # Invoke the drink information microservice
    print('\n-----Invoking drink_information microservice-----')
    drink_result = invoke_http(drinkinfo_URL, method='GET', json=drink)
    print('drink_result:', drink_result)

    # 5. Get the review for drink
    # Invoke the review microservice
    print('\n\n-----Invoking review microservice-----')
    review_result = invoke_http(
        review_URL, json=review_result['strDrink'])
    print("review_result:", review_result, '\n')

    # 7. Return created order, shipping record
    return {
        "code": 201,
        "data": {
            "drink_result": drink_result,
            "review_result": review_result
        }
    }

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for search drink...")
    app.run(host="0.0.0.0", port=5020, debug=True)