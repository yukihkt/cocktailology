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

    cocktail_URL = environ.get('cocktail_URL') or "http://localhost:5022/cocktail" + "/" + cocktail_name
    review_URL = environ.get('review_URL') or "http://localhost:5021/review" + "/" + cocktail_name
    
    
    cocktail_result = invoke_http(cocktail_URL, method="GET")
    review_result = invoke_http(review_URL, method="GET")

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