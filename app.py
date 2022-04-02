from flask import Flask,render_template,request, jsonify, url_for, session, redirect
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook

import requests

app = Flask(__name__)
app.config["SERVER_NAME"] = "localhost:5000"
app_id = "3173224822906874"
secret_id = "b40e76368df065f5447a9ffb74c950df"
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!/xd5\xa2\xa0\x9fR"\xa1\xa8'

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