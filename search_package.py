from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http
import json

app = Flask(__name__)
CORS(app)

@app.route("/search_package/<string:cocktail_name>")
def search_package(cocktail_name):
    if cocktail_name:
        try:
            cocktail_URL = environ.get('cocktail_URL') or "http://localhost:5022/cocktail" + "/" + cocktail_name
            review_URL = environ.get('review_URL') or "http://localhost:5021/review" + "/" + cocktail_name
    
            cocktail_result = invoke_http(cocktail_URL, method="GET")
            print('cocktail_result: ', cocktail_result)
            review_result = invoke_http(review_URL, method="GET")
            print('cocktail_result: ', cocktail_result)

            return {
                    "code": 201,
                    "data": {
                        "cocktail_result": cocktail_result,
                        "review_result": review_result
                    }
            }

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

    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for search package...")
    app.run(host="0.0.0.0", port=5020, debug=True)