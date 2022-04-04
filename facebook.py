from flask import Flask,render_template,request, jsonify, url_for, session, redirect
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)
app.config["SERVER_NAME"] = "localhost:9000"
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!/xd5\xa2\xa0\x9fR"\xa1\xa8'

###############################################################
facebook_bp = make_facebook_blueprint(
    client_id=os.getenv("app_id"),
    client_secret=os.getenv("secret_id"),
    redirect_to="fb_auth",
    scope='email')
app.register_blueprint(facebook_bp, url_prefix="/login")

@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/search_package')
def search_package():
    return render_template("search_package.html")

@app.route('/search_results')
def search_results():
    return render_template("search_results.html")

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/facebook')
def loggedin():
    return redirect(url_for("facebook.login"))

@app.route('/order_history')
def order_history():
    return render_template("account_pages/order_history.html")

@app.route('/account_details')
def account_details():
    return render_template("account_pages/account_details.html")

@app.route('/facebook/authorized')
def fb_auth():
    if not facebook.authorized:
        return redirect(url_for("homepage"))
    resp = facebook.get("/me?fields=name,id")
    assert resp.ok, resp.text
    session["name"] = resp.json().get('name')
    session["account_id"] = resp.json().get('id')
    return render_template("account_form.html", data = resp.json())

@app.route("/facebook/logout")
def fb_logout():
    session.clear()
    return redirect(url_for('homepage'))

############################################################

if __name__ == "__main__":
    app.run( port=9000, debug=True, ssl_context='adhoc')
