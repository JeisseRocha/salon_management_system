def non_empty_string(s):
    if not s:
        raise ValueError("Must not be empty string")
    return s


def card_validator(parser):
    parser.add_argument('card_number', help='card number required', required=True, nullable=False,
                        type=non_empty_string)
    parser.add_argument('service_name', help='service name required', required=True, nullable=False,
                        type=non_empty_string)
    parser.add_argument('price', help='service price required', required=True, nullable=False,
                        type=int)
    parser.add_argument('exp_month', help='expiration month required', required=True, nullable=False,
                        type=int)
    parser.add_argument('exp_year', help='expiration year required', required=True, nullable=False,
                        type=int)
    parser.add_argument('cvc', help='cvc required', required=True, nullable=False,
                        type=non_empty_string)
