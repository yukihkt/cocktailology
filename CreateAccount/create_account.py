# complex ms in use case 1, orchestrates data from account to email
# to test this ms, simultaneosly run email, amqp_setup and account ms in 3 separate CMD windows
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from Account.invokes import invoke_http

import CreateAccount.amqp_setup as amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

account_URL = "http://localhost:5000/account"



@app.route("/create_account", methods=['POST'])
def place_order():
    # Simple check of input format and data of the request are JSON
    if request.is_json: 
        try:
            new_account_details = request.get_json()
            print("\nReceived an account in JSON:", new_account_details)

            # do the actual work
            # 1. Send order info {cart items}
            result = processCreateAccount(new_account_details)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "create_account.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processCreateAccount(new_account_details):
    # 2. Send the order info {cart items}
    # Invoke the order microservice
    print('\n-----Invoking account microservice-----')
    account_creation_result = invoke_http(account_URL, method='POST', json=new_account_details)
    print('account_creation_result:', account_creation_result)
  

    # Check the order result; if a failure, send it to the error microservice.
    code = account_creation_result["code"]
    message = json.dumps(account_creation_result)

   
    if code not in range(200, 300):
        # TODO: for shub to error handle if fb acc doesnt exist?
        pass

    else:
        print('\n\n-----Publishing the (newly created account info) message with routing_key=create.success-----')        
        
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="create.success", 
            body=message)
    
    print("\nAccount details published to RabbitMQ Exchange.\n")
    # - reply from the invocation is not used;
    # continue even if this invocation fails

    return {
        "code": 201,
        "data": {
            "account_creation_result": account_creation_result
        }
    }


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for creating an account ...")
    app.run(host="0.0.0.0", port=5100, debug=True)