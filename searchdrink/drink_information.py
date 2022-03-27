from flask import Flask, render_template, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/search/<type>',methods=['GET', 'POST'])
def drink_information(type):
    selected_cocktail = type
    if request.method == 'GET':
        new_url = f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={selected_cocktail}'
        print('api_url 1', new_url)
        try:
            r = requests.get(new_url)
            data = r.json()
            print('data', data)
            array = data["drinks"]
            return render_template("cocktail_home.html", array=array,selected_cocktail=selected_cocktail)
        except:
            return "Unexpected Error Occurred"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5022, debug=True)