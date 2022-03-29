from flask import Flask,render_template,request, jsonify, url_for, session, redirect
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook

import requests

app = Flask(__name__)
app.config["SERVER_NAME"] = "localhost:5000"
app_id = "3173224822906874"
secret_id = "b40e76368df065f5447a9ffb74c950df"
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!/xd5\xa2\xa0\x9fR"\xa1\xa8'

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')


###############################################################
facebook_bp = make_facebook_blueprint(
    client_id=app_id,
    client_secret=secret_id,
    redirect_to="fb_auth",
    scope='email')
app.register_blueprint(facebook_bp, url_prefix="/login")

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/facebook')
def loggedin():
    return redirect(url_for("facebook.login"))


@app.route('/facebook/authorized')
def fb_auth():
    if not facebook.authorized:
        return redirect(url_for("homepage"))
    resp = facebook.get("/me?fields=name,id")
    assert resp.ok, resp.text
    session["name"] = resp.json().get('name')
    session["account_id"] = resp.json().get('id')
    return render_template("home.html", data = resp.json())

@app.route("/facebook/logout")
def fb_logout():
    session.clear()
    return redirect(url_for('homepage'))

############################################################

@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')

@app.route('/search',methods = ['POST'])
def getalcohol():
    if request.method == 'POST':
        value = request.form['search']
        print("value", value)
        api_url = f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={value}'
        print('api_url' ,api_url)
        try:
            r = requests.get(api_url)
            data = r.json()
            print('data',data)
            array = data["drinks"]
            print('array ', array)
            return render_template("cocktail_data.html",array=array,value=value)
        except:
            return " <h1> Oops.. No such cocktail found </h1>"

@app.route('/search/<type>',methods=['GET', 'POST'])

# Getting clicked data from url we used get
def cocktail_select(type):
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
    app.run(debug = True, ssl_context='adhoc')