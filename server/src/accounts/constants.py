class UserFieldLengths:
    FIRST_NAME_MAX = 30
    FIRST_NAME_MIN = 2

    LAST_NAME_MAX = 30
    LAST_NAME_MIN = 2

    PHONE_NUMBER_MAX = 15
    PHONE_NUMBER_MIN = 9

    USERNAME_MAX = 150

    COUNTRY_MAX = 100
    COUNTRY_MIN = 2

    CITY_MAX = 100
    CITY_MIN = 2

    ZIP_CODE_MAX = 10
    ZIP_CODE_MIN = 3

    STREET_ADDRESS_MAX = 100
    STREET_ADDRESS_MIN = 2

    APARTMENT_MAX = 20


class UserErrorMessages:
    EMAIL_UNIQUE = 'A user with this email already exists.'
    USERNAME_UNIQUE = 'A user with this username already exists.'
    AGREED_TO_EMAILS = 'You must agree to receive email updates.'
    INCORRECT_PASSWORD = 'Current password is incorrect.'
    NEW_PASSWORD_SAME_AS_CURRENT = (
        'New password must be different from current password.'
    )
    PASSWORD_NO_DIGIT = 'Your password must contain at least one digit.'
    PASSWORD_NO_UPPER_CASE_LETTER = (
        'Your password must contain at least one upper case letter.'
    )
    PASSWORD_NO_LOWER_CASE_LETTER = (
        'Your password must contain at least one lower case letter.'
    )
    PASSWORD_NO_WHITE_SPACES = 'Your password must not contain white spaces.'
    PASSWORD_NO_SPECIAL_CHAR = (
        'Your password must contain at least one special character (!#$%).'
    )
    INCORRECT_CREDENTIALS = 'Invalid username or password.'
    INVALID_TOKEN = 'Invalid or expired token'


class UserSuccessMessages:
    LOGOUT_SUCCESS = 'Logout successful.'
    PASSWORD_CHANGED = 'Password changed successfully.'
    RESET_LINK_SENT = 'A reset link has been sent.'
    PASSWORD_RESET = 'Password reset successful.'


class PhotoSize:
    MAX_SIZE = 5
