# test_invoke_http.py
from invokes import invoke_http


# invoke account microservice to get all accounts
results = invoke_http("http://localhost:5003/order", method='GET')

print( type(results) )
print()
print( results )

# invoke order microservice to create an order
order_id = '4'
order_details = {"account_id": 4, "created": "Sun, 12 Jun 2022 10:14:55 GMT", "orderStatus": "NEW", "order_id": 4, "cart_item": [{"item_id": 8, "order_id": 4, "packageName": "Drink1", "quantity": 1}, {"item_id": 9, "order_id": 4, "packageName": "Drink2", "quantity": 1}]}
create_results = invoke_http(
        "http://localhost:5003/order" + "/" + order_id, method='POST', 
        json=order_details
    )

print()
print( create_results )
