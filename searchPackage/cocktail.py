import sys
import os
from os import environ

from flask import Flask, request, jsonify
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('cocktail_URL') or 'mysql+mysqlconnector://root:root@localhost:3306/cocktail'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app) 
 
class Cocktail(db.Model):
    __tablename__ = 'cocktail'
 
    cocktail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cocktail_name = db.Column(db.String(30), nullable=False)
    cocktail_price = db.Column(db.String(8), nullable=False)
    cocktail_description = db.Column(db.String(300), nullable=False)
    cocktail_recipe = db.Column(db.String(300), nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)
    def json(self):
        dto = {
            'cocktail_id': self.cocktail_id,
            'cocktail_name': self.cocktail_name, 
            'cocktail_price' : self.cocktail_price,
            'cocktail_description' : self.cocktail_description,
            'cocktail_recipe' : self.cocktail_recipe,
            'quantity_available': self.quantity_available
        }

        dto['cocktail_ingredients'] = []
        for ci in self.cocktail_ingredients:
            dto['cocktail_ingredients'].append(ci.json())

        return dto

class Cocktail_Ingredients(db.Model):
    __tablename__ = 'cocktail_ingredients'

    c_ingredients_id = db.Column(db.Integer, primary_key=True)
    cocktail_id = db.Column(db.ForeignKey(
        'cocktail.cocktail_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    c_ingredients = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)

    # order_id = db.Column(db.String(36), db.ForeignKey('order.order_id'), nullable=False)
    # order = db.relationship('Order', backref='order_item')
    cocktail = db.relationship(
        'Cocktail', primaryjoin='Cocktail_Ingredients.cocktail_id == Cocktail.cocktail_id', backref='cocktail_ingredients')

    def json(self):
        return {'c_ingredients_id': self.c_ingredients_id, 'cocktail_id': self.cocktail_id, 'c_ingredients': self.c_ingredients, 'quantity': self.quantity}


@app.route("/cocktail")
def get_all():
    cocktaillist = Cocktail.query.all()
    if len(cocktaillist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "cocktail": [cocktail.json() for cocktail in cocktaillist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no cocktails."
        }
    )

@app.route("/cocktail/<string:cocktail_name>")
def find_by_cocktail_name(cocktail_name):
    cocktail = Cocktail.query.filter_by(cocktail_name=cocktail_name).first()
    if cocktail:
        return jsonify(
            {
                "code": 200,
                "data": cocktail.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "cocktail_name": cocktail_name
            },
            "message": "Cocktail not found."
        }
    ), 404


#for quantity 
@app.route("/cocktail/<int:cocktail_id>")
def find_qty_cocktail_id(cocktail_id):
    cocktail = Cocktail.query.filter_by(cocktail_id=cocktail_id).first()
    if cocktail:
        return jsonify(
            {
                "code": 200,
                "data": cocktail.quantity_available
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "cocktail_id": cocktail_id
            },
            "message": "Cocktail not found."
        }
    ), 404

    #need to create a form to see how many order someone wants to make 



if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": cocktail information...")
    app.run(host='0.0.0.0', port=5022, debug=True)