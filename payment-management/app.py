
import stripe
import os

from flask import Flask, render_template, jsonify, request, send_from_directory, redirect, make_response
from dotenv import load_dotenv, find_dotenv


# Setup Stripe python client library.
load_dotenv(find_dotenv())

# Ensure environment variables are set.
# price = os.getenv('PRICE')
# if price is None or price == 'price_12345' or price == '':
#     print('You must set a Price ID in .env. Please see the README.')
#     exit(0)


# stripe.api_version = '2022-04-04'
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

static_dir = str(os.path.abspath(os.path.join(
    __file__, "..", os.getenv("STATIC_DIR"))))
app = Flask(__name__, static_folder=static_dir,
            static_url_path="", template_folder=static_dir)


@app.route('/', methods=['GET'])
def get_example():
    return render_template('/index.html')


@app.route('/config', methods=['GET'])
def get_publishable_key():
    price = stripe.Price.retrieve(os.getenv('PRICE'))
    return jsonify({
        'publicKey': os.getenv('STRIPE_PUBLISHABLE_KEY'),
        'unitAmount': price['unit_amount'],
        'currency': price['currency']
    })


# Fetch the Checkout Session to display the JSON result on the success page
@app.route('/checkout-session', methods=['GET'])
def get_checkout_session():
    id = request.args.get('sessionId')
    checkout_session = stripe.checkout.Session.retrieve(id)
    return jsonify(checkout_session)


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    quantity = request.form.get('quantity', 1)
    price = request.args.get('price')
    domain_url = os.getenv('DOMAIN')

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + '/success.html?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain_url + '/canceled.html',
            mode='payment',
            line_items=[{
                'price': price,
                'quantity': quantity,
            }]
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)


if __name__ == '__main__':
    app.run(port=4242, debug=True)
