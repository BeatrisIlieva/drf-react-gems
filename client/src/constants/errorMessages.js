import { FIELD_LENGTHS } from "./fieldLengths";

export const AUTH_ERROR_MESSAGES = {
    PASSWORD:
        "Sorry, the provided password does not match the required constraints",
    EMAIL: "Please enter a valid email address",
    USERNAME: `Username must be ${FIELD_LENGTHS.USERNAME_MIN}-${FIELD_LENGTHS.USERNAME_MAX} characters long and contain only letters, numbers, and underscores`,
    EMAIL_OR_USERNAME: "Please enter a valid email address or username",
};

export const PERSONAL_INFO_ERROR_MESSAGES = {
    NAME: `Name must contain only letters and be ${FIELD_LENGTHS.FIRST_NAME_MIN}-${FIELD_LENGTHS.FIRST_NAME_MAX} characters long`,
    PHONE: `Phone number must be ${FIELD_LENGTHS.PHONE_NUMBER_MIN}-${FIELD_LENGTHS.PHONE_NUMBER_MAX} digits long`,
};

export const ADDRESS_ERROR_MESSAGES = {
    COUNTRY_TOO_SHORT: `Country must be at least ${FIELD_LENGTHS.COUNTRY_MIN} characters`,
    COUNTRY_TOO_LONG: `Country cannot exceed ${FIELD_LENGTHS.COUNTRY_MAX} characters`,
    COUNTRY_INVALID_CHARS: "Country must contain only letters and spaces",
    CITY_TOO_SHORT: `City must be at least ${FIELD_LENGTHS.CITY_MIN} characters`,
    CITY_TOO_LONG: `City cannot exceed ${FIELD_LENGTHS.CITY_MAX} characters`,
    CITY_INVALID_CHARS: "City must contain only letters and spaces",
    ZIP_CODE_TOO_SHORT: `ZIP code must be at least ${FIELD_LENGTHS.ZIP_CODE_MIN} characters`,
    ZIP_CODE_TOO_LONG: `ZIP code cannot exceed ${FIELD_LENGTHS.ZIP_CODE_MAX} characters`,
    STREET_ADDRESS_TOO_SHORT: `Street address must be at least ${FIELD_LENGTHS.STREET_ADDRESS_MIN} characters`,
    STREET_ADDRESS_TOO_LONG: `Street address cannot exceed ${FIELD_LENGTHS.STREET_ADDRESS_MAX} characters`,
    APARTMENT_TOO_LONG: "Apartment number is too long",
};
