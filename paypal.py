
#paypal wrapper

from flask import Flask, render_template, jsonify, request, redirect
import paypalrestsdk

app = Flask(__name__)



paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "ARInOSQswDDw2JXnDpyAdDTs9Dgdf9tNDBUq-MSC9nRRICQrPXh7p8XiGYsqJlDin-j5oe6ZKN8P-Yrt",
  "client_secret": "EOOuzw2fQH3aKlrRRNts_mR3nNu_wjuuXShoKKZ_lP3R0KBMndy203bPiBssayygnLqZMH4mV4VR11Cg" })

@app.route('/')
def index():
    return render_template('paypal.html') 

@app.route('/payment', methods=['POST'])
def payment():

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "testitem",
                    "price": "500.00",
                    "currency": "SGD",
                    "quantity": 1}]},
            "amount": {
                "total": "500.00",
                "currency": "SGD"},
                }]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
        return redirect("orderconfirm.html")
        
    else:
        print(payment.error)

    return jsonify({'success' : success})

if __name__ == '__main__':
    app.run(debug=True)