import os

import stripe
from dotenv import load_dotenv
from werkzeug.exceptions import InternalServerError

load_dotenv()

STRIPE_SECRET = os.environ.get("STRIPE_SECRET")

stripe.api_key = STRIPE_SECRET


def pay(amount, product, card_number, exp_month, exp_year, cvc):
    token = generate_token(card_number, exp_month, exp_year, cvc)
    return charge(product=product, amount=int(amount), token_id=token.id)


def generate_token(card_number, exp_month, exp_year, cvc):
    try:
        return stripe.Token.create(
            card={
                "number": card_number,
                "exp_month": exp_month,
                "exp_year": exp_year,
                "cvc": cvc,
            },
        )
    except Exception as e:
        raise InternalServerError("Internal Server")


def charge(product, amount, token_id):
    try:
        return stripe.Charge.create(
            amount=amount * 100,
            currency="eur",
            source=token_id,
            description=product,
        )
    except Exception as e:
        raise InternalServerError("Internal Server")
