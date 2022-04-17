from werkzeug.exceptions import NotFound

from src import payment, dynamo


def save_payment(args):
    card_number = args['card_number']
    exp_month = args['exp_month']
    exp_year = args['exp_year']
    cvc = args['cvc']
    service_name = args['service_name']
    price = args['price']

    response = payment.pay(price, service_name, card_number, exp_month, exp_year, cvc)

    strip_id = response.stripe_id
    amount = (response.amount / 100)
    receipt_url = response.receipt_url
    is_refunded = response.refunded
    status = response.status
    paid = response.paid
    failure_code = response.failure_code
    failure_message = response.failure_message

    dynamo.save_payment(payment_id=strip_id, amount=str(amount), receipt_url=receipt_url, is_refunded=is_refunded,
                        paid=paid,
                        status=status, failure_message=failure_message, failure_code=failure_code)

    return receipt_url


def get_payments():
    return dynamo.get_payments()


def get_payment(payment_id):
    payment_payload = dynamo.get_payment(payment_id)
    if "Item" not in payment_payload:
        raise NotFound("booking not  found")
    return payment_payload['Item']
