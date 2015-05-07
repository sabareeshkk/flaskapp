from flask import Flask, jsonify
from flask import render_template
import braintree
from flask import request
from braintree.configuration import Configuration
app = Flask(__name__)


braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    merchant_id="qn5442rvm794nc6q",
    public_key="m39g67q6hrg23dhv",
    private_key="818879cf109847fb106192b48078b969")


@app.route("/")
def hello():
    result = braintree.Customer.create({
            "id": "sabareeshk",
            "company": "Some company",
            "email": "john.doe@example.com",
            "fax": "123-555-1212",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "123-555-1221",
            "website": "http://www.example.com",
            "credit_card": {
                "cardholder_name": "John Doe",
                "cvv": "123",
                "expiration_date": "12/2012",
                "number": "4111111111111111",
                "token": "sab",
                "billing_address": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "company": "Braintree",
                    "street_address": "111 First Street",
                    "extended_address": "Unit 1",
                    "locality": "Chicago",
                    "postal_code": "60606",
                    "region": "IL",
                    "country_name": "United States of America"
                },
                "options": {
                    "verify_card": True
                }
            }
        })
    print result
    return render_template('index.html', result=result)


@app.route("/client_token")
def client_token():
    result = braintree.ClientToken.generate()
    print result
    result = braintree.MerchantAccount.create({
        'individual': {
            'first_name': "Jane",
            'last_name': "Doe",
            'email': "jane@14ladders.com",
            'phone': "5553334444",
            'date_of_birth': "1981-11-19",
            'ssn': "456-45-4567",
            'address': {
                'street_address': "111 Main St",
                'locality': "Chicago",
                'region': "IL",
                'postal_code': "60622"
            }
        },
        'funding': {
            'descriptor': "Blue Ladders",
            'destination': braintree.MerchantAccount.FundingDestination.Bank,
            'email': "funding@blueladders.com",
            'mobile_phone': "5555555555",
            'account_number': "1123581321",
            'routing_number': "071101307",
        },
        "tos_accepted": True,
        "master_merchant_account_id": "32wqzgkfytb5xhhd",
        "id": "blue_ladders_store"
    })
    print result.is_success

    return render_template("brain.html", result=result)

@app.route("/checkout", methods=['POST'])
def checkout():
    if request.method == 'POST':
        print request.form['payment_method_nonce']



    #     result = braintree.Customer.create({
    # "first_name": "Charity",
    # "last_name": "Smith",
    # "payment_method_nonce": request.form['payment_method_nonce']
    #   })
    
        # result = braintree.PaymentMethod.create({
        #     "customer_id": "the_customer_id",
        #     "payment_method_nonce": request.form['payment_method_nonce'],
            
        # })
        

        result = braintree.Transaction.sale({
        "amount": "10000.00",
        "order_id": "order id",
        "merchant_account_id": "blue_ladders_store",
        "service_fee_amount": '100',
        "credit_card": {
                    "number": "4111111111111111",
                    "expiration_date": "12/2012"
                },
        "options": {
            "submit_for_settlement": True,
            "store_in_vault_on_success": True
        },
        "channel": "MyShoppingCartProvider"
    })

        print result
        return "hello world"



if __name__ == "__main__":
    app.run(debug=True)
