import os
from email.policy import default

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Table

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/shipping_record'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
class Shipping_Record(db.Model):

    __tablename__ = 'shipping_record'

    shippingID = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    shippingAddress = db.Column(db.String(100), nullable=False)
    shippingDate = db.Column(db.DateTime(timezone=True), nullable=False)
    shippingDescription = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False, default="pending")
    orderID =db.Column(db.Integer, ForeignKey('order_id'))

    def __init__(self, shippingID, shippingAddress, shippingDate, shippingDescription, status, orderID):
        self.shippingID = shippingID
        self.shippingAddress = shippingAddress
        self.shippingDate = shippingDate
        self.shippingDescription = shippingDescription
        self.status = status
        self.orderID = orderID

    def json(self):
        return {"shippingID": self.shippingID, "shippingAddress": self.shippingAddress, "shippingDate": self.shippingDate, "shippingDescription": self.shippingDescription, "status": self.status, "orderID":self.orderID}


db.create_all()
@app.route("/shipping_record", methods=['POST'])
def receiveOrder():
    if request.is_json:
        order = request.get_json()
        result = processOrder(order)
        return jsonify(result), result["code"]
    else:
        data = request.get_data()
        print("Received an invalid order:")
        print(data)
        return jsonify({"code": 400,
                        "data": str(data),
                        "message": "Order should be in JSON."}), 400 


def processOrder(order):
    print("Processing an order for shipping:")

    #to check if there is a shipping record attached to the current order
    if db.session.query(Shipping_Record).filter_by(orderID=order['order_id']).count() > 0:
        return {
            'code': 400,
            'data': {
                'order_id': order['order_id']
            },
            'message': 'order already has a shipping record'
        }

    # creating the database entry record (eg. shipping_address from order form)
    new_record = Shipping_Record(shippingAddress=order['shipping_address'], shippingDate=order['shipping_date'], shippingDescription=order['shipping_description'], status="pending", orderID=order['order_id'], shippingID=order['shipping_id'] )
    db.session.add(new_record) #adding the entry to the database
    db.session.commit()
    
    return {
        'code': 200,
        'data': {
            'order_id': order['order_id']
        },
        'message': 'order successfully submitted !!!'
    }


# execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
        ": shipping for orders ...")
    app.run(host='0.0.0.0', port=5033, debug=True)
