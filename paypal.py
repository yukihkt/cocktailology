
import os
from flask import Flask, render_template, jsonify, request, redirect
import paypalrestsdk
from invokes import invoke_http
from flask_cors import CORS
import paypalrestsdk


app = Flask(__name__)
CORS(app) 

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "ARInOSQswDDw2JXnDpyAdDTs9Dgdf9tNDBUq-MSC9nRRICQrPXh7p8XiGYsqJlDin-j5oe6ZKN8P-Yrt",
  "client_secret": "EOOuzw2fQH3aKlrRRNts_mR3nNu_wjuuXShoKKZ_lP3R0KBMndy203bPiBssayygnLqZMH4mV4VR11Cg" })



@app.route('/payment', methods=['POST'])
def payment():
    account_id = request.json.get('account_id', None)
    accountURL = "http://localhost:5013/account/" + str(account_id)
    res = invoke_http(accountURL)
    cart = res['data']['cart']

    totalPayment = request.json.get('total', None)
    print("totalPayment: ", totalPayment)

    deliveryPayment = request.json.get('delivery', None)
    cart.append({"name": "delivery", "price": deliveryPayment, "quantity": 1, "currency": "SGD"})
    print("cart: ", cart)


    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {

                "items": cart
            },
            "amount": {
                "total": totalPayment,
                "currency": "SGD"},
            }]})

    if payment.create():
        print('Payment success!')
        return jsonify({ "code": 200, "message": "success" })
    else:
        print(payment.error)
        return jsonify({ "code": 400, "message": "error" })

    # return jsonify({'paymentID' : payment.id})


@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True

        
    else:
        print(payment.error)

    return jsonify({'success' : success})

if __name__ == '__main__':

    print("This is flask for " + os.path.basename(__file__) + ": payment ...")
    app.run(host='0.0.0.0', port=5014, debug=True)

