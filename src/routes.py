from flask_restful import Api

from src.payment_resource import PaymentResource,PaymentItemResource


def register_routes(app):
    api = Api(app)

    api.add_resource(PaymentResource, '/api/payments')
    api.add_resource(PaymentItemResource, '/api/payments/<string:payment_id>')

