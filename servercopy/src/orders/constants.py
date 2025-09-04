class CardFieldLengths:
    CARD_NUMBER_MAX_LENGTH = 19
    CARD_NUMBER_EXACT_LENGTH = 16

    CARD_HOLDER_NAME_MAX_LENGTH = 50
    CARD_HOLDER_NAME_MIN_LENGTH = 2

    EXPIRY_DATE_MAX_LENGTH = 5
    EXPIRY_DATE_EXACT_LENGTH = 5

    CVV_MAX_LENGTH = 3
    CVV_EXACT_LENGTH = 3


class CardErrorMessages:
    INVALID_CARD_NUMBER = 'Please enter a valid card number'

    INVALID_CARD_HOLDER_NAME = 'Please enter a valid name'

    INVALID_CVV_CODE = 'Please enter a valid security code'

    INVALID_EXPIRY_DATE = 'Please enter a valid expiry date (MM/YY)'

    CARD_HAS_EXPIRED = 'Card has expired'


class CardRegexPatterns:
    VISA = r'^4[0-9]{3} [0-9]{4} [0-9]{4} [0-9]{4}$'
    MASTERCARD_LEGACY = r'^5[1-5][0-9]{2} [0-9]{4} [0-9]{4} [0-9]{4}$'
    MASTERCARD_NEW = r'^(222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720) [0-9]{4} [0-9]{4} [0-9]{4}$'
    CVV = rf'^[0-9]{{{CardFieldLengths.CVV_EXACT_LENGTH}}}$'
    EXPIRY_DATE = r'^(0[1-9]|1[0-2])/([0-9]{2})$'
    CARD_HOLDER = rf"^[A-Za-z\u00C0-\u024F'\- ]{{{CardFieldLengths.CARD_HOLDER_NAME_MIN_LENGTH},{CardFieldLengths.CARD_HOLDER_NAME_MAX_LENGTH}}}$"


class OrderStatusMessages:
    STATUS_CREATED = 'Order completed successfully'
    STATUS_NO_ORDERS = 'No orders created'


class OrderErrorMessages:
    ERROR_INVALID_CONTENT_TYPE_OR_ID = 'Invalid content type or object ID'
    ERROR_REVIEW_NOT_FOUND = 'Review not found'
