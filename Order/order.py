#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/order'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)  

class Order(db.Model):
    __tablename__ = 'order'

    order_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, nullable=False)
    orderStatus = db.Column(db.String(10), nullable=False) 
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    

    def json(self):
        dto = {
            'order_id': self.order_id,
            'account_id': self.account_id,
            'orderStatus': self.orderStatus,
            'created': self.created,
            
        }

        dto['order_item'] = []
        for oi in self.order_item:
            dto['order_item'].append(oi.json())

        return dto


class Order_Item(db.Model):
    __tablename__ = 'order_item'

    item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.ForeignKey(
        'order.order_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    packageName= db.Column(db.String(64), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # order_id = db.Column(db.String(36), db.ForeignKey('order.order_id'), nullable=False)
    # order = db.relationship('Order', backref='order_item')
    order = db.relationship(
        'Order', primaryjoin='Order_Item.order_id == Order.order_id', backref='order_item')

    def json(self):
        return {'item_id': self.item_id, 'packageName': self.packageName, 'quantity': self.quantity, 'order_id': self.order_id}


@app.route("/order")
def get_all():
    orderlist = Order.query.all()
    if len(orderlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "orders": [order.json() for order in orderlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no orders."
        }
    ), 404


@app.route("/order/<string:order_id>")
def find_by_order_id(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if order:
        return jsonify(
            {
                "code": 200,
                "data": order.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "order_id": order_id
            },
            "message": "Order not found."
        }
    ), 404


@app.route("/order", methods=['POST'])
def create_order():
    account_id = request.json.get('account_id', None)
    order = Order(account_id=account_id, orderStatus='NEW')

    cart_item = request.json.get('cart_item')
    for item in cart_item:
        order.order_item.append(Order_Item(
            packageName=item['packageName'], quantity=item['quantity']))

    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the order. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": order.json()
        }
    ), 201


@app.route("/order/<string:order_id>", methods=['PUT'])
def update_order(order_id):
    try:
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "order_id": order_id
                    },
                    "message": "Order not found."
                }
            ), 404

        # update status
        data = request.get_json()
        if data['status']:
            order.status = data['status']
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": order.json()
                    
                }
            ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "order_id": order_id
                },
                "message": "An error occurred while updating the order. " + str(e)
            }
        ), 500


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage orders ...")
    app.run(host='0.0.0.0', port=5003, debug=True)
