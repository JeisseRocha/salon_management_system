import datetime
import os

from boto3 import resource
from dotenv import load_dotenv
from werkzeug.exceptions import InternalServerError

load_dotenv()

AWS_ACCESS_KEY_ID = os.environ["ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["SECRET_ACCESS_KEY"]
REGION_NAME = os.environ["REGION_NAME"]

resource = resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)

PaymentTable = resource.Table('S_PAYMENTS')


def save_payment(payment_id: str, amount: str, receipt_url: str, is_refunded: bool, paid: bool, status: bool,
                 failure_code, failure_message):
    try:
        return PaymentTable.put_item(
            Item={
                'id': payment_id,
                'amount': amount,
                'receipt_url': receipt_url,
                'is_refunded': is_refunded,
                'paid': paid,
                'status': status,
                'failure_code': failure_code,
                'failure_message': failure_message,
                "payment_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            }
        )
    except Exception as e:
        print(e)
        raise InternalServerError("Internal server error")


def get_payments():
    try:
        response = PaymentTable.scan()
        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = PaymentTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        return data
    except Exception as e:
        print(e)
        raise InternalServerError("Internal server error")


def get_payment(payment_id: str):
    try:
        return PaymentTable.get_item(
            Key={'id': payment_id})
    except Exception as e:
        print(e)
        raise InternalServerError("Internal server error")
