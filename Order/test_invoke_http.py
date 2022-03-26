# test_invoke_http.py
from invokes import invoke_http

# invoke account microservice to get all accounts
results = invoke_http("http://localhost:5003/order", method='GET')

print( type(results) )
print()
print( results )

# invoke order microservice to create an order
order_id = '2'
order_details = { "account_id": "2", "orderStatus": "NEW", "created": "2022-06-12 02:14:55" }
create_results = invoke_http(
        "http://localhost:5003/order/" + order_id, method='POST', 
        json=order_details
    )

print()
print( create_results )
