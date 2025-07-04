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
