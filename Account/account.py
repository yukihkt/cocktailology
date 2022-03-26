# !!dummy microservice made by andrea to do complex microservice create_account
# TODO: for shub to replace

import os
# from os import environ
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


# from datetime import datetime
# import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/account'
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# set dbURL=mysql+mysqlconnector://root@localhost:3306/account
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)  

class Account(db.Model):
    __tablename__ = 'account'

    account_id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    shipping_add = db.Column(db.String(100), nullable=False)

    # status = db.Column(db.String(10), nullable=False)
    # created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # modified = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, account_id , account_name, shipping_add, email):
        self.account_id = account_id
        self.account_name = account_name
        self.shipping_add = shipping_add
        self.email = email

    def json(self):
        return {
            'account_id': self.account_id,
            'account_name': self.account_name,
            'shipping_add': self.shipping_add,
            'email': self.email
            # 'created': self.created,
            # 'modified': self.modified
        }


@app.route("/account")
def get_all():
    accountlist = Account.query.all()
    if len(accountlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "accounts": [account.json() for account in accountlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no accounts."
        }
    ), 404

@app.route("/account/<string:account_id>")
def find_by_accountid(account_id):
    account = Account.query.filter_by(account_id=account_id).first()
    if account:
        return jsonify(
            {
                "code": 200,
                "data": account.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Account not found."
        }
    ), 404


# TODO: for shub to adjust, since login and signin same for fb (for now??) maybe redirect user straightaway to home page in the first if statement
@app.route("/book/<string:account_id>", methods=['POST'])
def create_book(account_id):
    if (Account.query.filter_by(account_id=account_id).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "account_id": account_id
                },
                "message": "Account already exists."
            }
        ), 400

    data = request.get_json()
    account = Account(account_id, **data)

    try:
        db.session.add(account)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "account_id": account_id
                },
                "message": "An error occurred creating the account."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": account.json()
        }
    ), 201


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage accounts ...")
    app.run(host='0.0.0.0', port=5000, debug=True, verify=False)
