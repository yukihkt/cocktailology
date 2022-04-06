from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

account_URL = "http://localhost:5013/account" 
shipping_record_URL = "http://localhost:5033/shipping_record" 
order_URL = "http://localhost:5031/order"
cocktail_URL = "http://localhost:5022/cocktail"

@app.route("/place_order", methods=['POST'])
def place_order():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            order = request.get_json()
            print("\nReceived an order in JSON:", order)
            result = processCocktailCheck(order)
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
                "message": "place_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processCocktailCheck(order):
    print('\n-----Invoking cocktail microservice-----')
    print(type(order))
    # cart_items = json.dumps(order['cart_item'])
    cart_items = order['cart_item']
    print( type(cart_items),cart_items )
    cocktail_result = invoke_http(cocktail_URL, method='PUT', json=cart_items)
    print('cocktail_result:', cocktail_result)

    # return cocktail_result

    code = cocktail_result["code"]
    # message = json.dumps(cocktail_result)
    status = cocktail_result["data"]


    amqp_setup.check_setup()
    if code not in range(200, 300):
        # 7. Return error
        return {
            "code": 500,
            "data": {"inventory_result": cocktail_result},
            "message": "Internal server error when updating inventory stock."
        }
    else:
        print('\n\n-----Inventory low, attempting to call amqp-----')
        # action_email = 2: send email to 2 diff people
        if status!="success":
            message2 = json.loads('{"code":201,"message": "Inventory low"}')
            account_id = order['account_id']
            account_id = str(account_id)
            account_result = invoke_http(account_URL+'/'+account_id, method='GET')
            
            print('account_result:', account_result)

            # return cocktail_result
            code = account_result["code"]

            amqp_setup.check_setup()
            if code not in range(200, 300):
                # 7. Return error
                return {
                    "code": 500,
                    "data": {"account_result": account_result},
                    "message": "Internal server error when getting account details."
                }
            else:
                print('\n\n-----Publishing the (low inventory) message with routing_key=try.email-----')
                message2["email"] = account_result['data']['email']
                message2["account_name"] = account_result['data']['account_name']
                message2["email_action"] = "2"
                print("Publishing inventory low amqp queue")
                message2 = json.dumps(message2)
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="try.email",
                    body=message2, properties=pika.BasicProperties(delivery_mode = 2))      
                print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
                    code), cocktail_result)
                return {
                    "code": 200,
                    "message": "Inventory is low, email sent"
                }
        else:
            # call order
            order_result = processPlaceOrder(order)

            shipping_result = invoke_http(
                shipping_record_URL, method="POST", json=order['cart_item'])
            print("shipping_result:", shipping_result, '\n')

            code = shipping_result["code"]
            if code not in range(200, 300):
                # TODO: change the action_email
                message = json.dumps(shipping_result)
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="shipping.error", 
                    body=message, properties=pika.BasicProperties(delivery_mode = 2))

                print("\nShipping status ({:d}) published to the RabbitMQ Exchange:".format(
                    code), shipping_result)

                # 7. Return error
                
                return {
                    "code": 400,
                    "data": {
                        "order_result": order_result,
                        "shipping_result": shipping_result
                    },
                    "message": "Simulated shipping record error sent for error handling."
                }

            # 7. Return created order, shipping record
            return {
                "code": 201,
                "data": {
                    "order_result": order_result,
                    "shipping_result": shipping_result
                }
            }


def processPlaceOrder(order):
    print('\n-----Invoking order microservice-----')

    order_result = invoke_http(order_URL, method='POST', json=order)
    print('order_result:', order_result)
  
    code = order_result["code"]
    message = json.dumps(order_result)

    amqp_setup.check_setup()

    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as order fails-----')
        # print('\n\n-----Publishing the (order error) message with routing_key=order.error-----')

        # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.error", 
        #     body=message, properties=pika.BasicProperties(delivery_mode = 2))      
        # print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
        #     code), order_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"order_result": order_result},
            "message": "Order creation failure sent for error handling."
        }

    else:
        print('\n\n-----Publishing the (order info) message with routing_key=order.info-----')        

        # invoke_http(activity_log_URL, method="POST", json=order_result)            
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.info", 
            body=message)
    
    print("\nOrder published to RabbitMQ Exchange.\n")
    print('\n\n-----Invoking shipping_record microservice-----')    
    
    shipping_result = invoke_http(
        shipping_record_URL, method="POST", json=order_result['data'])
    print("shipping_result:", shipping_result, '\n')

    # Check the shipping result;
    # if a failure, send it to the error microservice.
    code = shipping_result["code"]
    if code not in range(200, 300):
        return {
            "code": 400,
            "data": {
                "order_result": order_result,
                "shipping_result": shipping_result
            },
            "message": "Simulated shipping record error."
        }

    return {
        "code": 201,
        "data": {
            "order_result": order_result,
            "shipping_result": shipping_result
        }
    }

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5030, debug=True)
