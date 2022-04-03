# test_invoke_http.py
from invokes import invoke_http


# invoke cocktail microservice to get all accounts
# results = invoke_http("http://localhost:5022/cocktail", method='GET')
# result_s = invoke_http("http://localhost:5021/review", method='GET')

# print( type(results) )
# print()
# print( results )
# print( result_s )

# invoke cocktail microservice to find review
cocktail_name = 'Vesper'
create_results = invoke_http(
        "http://localhost:5020/search_package" + "/" + cocktail_name)

print()
print( create_results )
