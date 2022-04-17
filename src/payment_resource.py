import http

from flask_restful import reqparse, Resource

from src import service
from src.validation import card_validator


class PaymentResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def post(self):
        card_validator(self.parser)
        args = self.parser.parse_args(http_error_code=422)
        receipt = service.save_payment(args)
        return {"receipt": receipt}, http.HTTPStatus.OK

    def get(self):
        return service.get_payments()


class PaymentItemResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)

    def get(self, payment_id):
        return service.get_payment(payment_id)
