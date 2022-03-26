# test_invoke_http.py
from Account.invokes import invoke_http

# invoke account microservice to get all accounts
results = invoke_http("http://localhost:5000/account", method='GET')

print( type(results) )
print()
print( results )

# invoke account microservice to create an account
account_id = '2'
account_details = { "account_name": "andrea2", "shipping_add": "Blk 123 Tampines Avenue 1\r\n#12-345\r\nS(123 456)\r\n", "email": "andreayupp@gmail.com" }
create_results = invoke_http(
        "http://localhost:5000/account/" + account_id, method='POST', 
        json=account_details
    )

print()
print( create_results )
