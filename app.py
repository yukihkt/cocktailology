from flask import Flask, render_template, jsonify, request
import paypalrestsdk

app = Flask(__name__)

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "ARInOSQswDDw2JXnDpyAdDTs9Dgdf9tNDBUq-MSC9nRRICQrPXh7p8XiGYsqJlDin-j5oe6ZKN8P-Yrt",
  "client_secret": "EOOuzw2fQH3aKlrRRNts_mR3nNu_wjuuXShoKKZ_lP3R0KBMndy203bPiBssayygnLqZMH4mV4VR11Cg" })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def homepage():
    return render_template('home.html')

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
                    "sku": "12345",
                    "price": "500.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "500.00",
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

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
    else:
        print(payment.error)

    return jsonify({'success' : success})


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

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
    app.run(debug = True)