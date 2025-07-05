import { FIELD_LENGTHS } from '../constants/fieldLengths';
import { PAYMENT_CONSTANTS } from '../constants/paymentConstants';
import {
    AUTH_ERROR_MESSAGES,
    PERSONAL_INFO_ERROR_MESSAGES,
    ADDRESS_ERROR_MESSAGES
} from '../constants/errorMessages';

export const validators = {
    email: {
        isValid: (value) =>
            /^[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/i.test(
                value
            )
                ? ''
                : AUTH_ERROR_MESSAGES.EMAIL
    },
    username: {
        isValid: (value) =>
            new RegExp(
                `^[A-Za-z0-9_]{${FIELD_LENGTHS.USERNAME_MIN},${FIELD_LENGTHS.USERNAME_MAX}}$`
            ).test(value)
                ? ''
                : AUTH_ERROR_MESSAGES.USERNAME
    },
    email_or_username: {
        isValid: (value) => {
            const isEmail =
                /^[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/i.test(
                    value
                );
            const isUsername = new RegExp(
                `^[A-Za-z0-9_]{${FIELD_LENGTHS.USERNAME_MIN},${FIELD_LENGTHS.USERNAME_MAX}}$`
            ).test(value);

            return isEmail || isUsername
                ? ''
                : AUTH_ERROR_MESSAGES.EMAIL_OR_USERNAME;
        }
    },
    password: {
        length: (password) =>
            password.length >= FIELD_LENGTHS.PASSWORD_MIN
                ? ''
                : AUTH_ERROR_MESSAGES.PASSWORD,

        upper: (password) =>
            /[A-Z]/.test(password)
                ? ''
                : AUTH_ERROR_MESSAGES.PASSWORD,

        lower: (password) =>
            /[a-z]/.test(password)
                ? ''
                : AUTH_ERROR_MESSAGES.PASSWORD,

        number: (password) =>
            /\d/.test(password)
                ? ''
                : AUTH_ERROR_MESSAGES.PASSWORD,

        noSpaces: (password) =>
            !/\s/.test(password)
                ? ''
                : AUTH_ERROR_MESSAGES.PASSWORD,

        special: (password) =>
            /[!#$%]/.test(password)
                ? ''
                : AUTH_ERROR_MESSAGES.PASSWORD
    },
    firstName: {
        isValid: (value) =>
            new RegExp(
                `^[A-Za-z]{${FIELD_LENGTHS.FIRST_NAME_MIN},${FIELD_LENGTHS.FIRST_NAME_MAX}}$`
            ).test(value)
                ? ''
                : PERSONAL_INFO_ERROR_MESSAGES.NAME
    },
    lastName: {
        isValid: (value) =>
            new RegExp(
                `^[A-Za-z]{${FIELD_LENGTHS.LAST_NAME_MIN},${FIELD_LENGTHS.LAST_NAME_MAX}}$`
            ).test(value)
                ? ''
                : PERSONAL_INFO_ERROR_MESSAGES.NAME
    },
    phoneNumber: {
        isValid: (value) =>
            new RegExp(
                `^\\d{${FIELD_LENGTHS.PHONE_NUMBER_MIN},${FIELD_LENGTHS.PHONE_NUMBER_MAX}}$`
            ).test(value)
                ? ''
                : PERSONAL_INFO_ERROR_MESSAGES.PHONE
    },
    currentPassword: {
        length: (password) =>
            password.length >= FIELD_LENGTHS.PASSWORD_MIN
                ? ''
                : AUTH_ERROR_MESSAGES.PASSWORD,

        upper: (password) =>
            /[A-Z]/.test(password)
                ? ''
                : AUTH_ERROR_MESSAGES.PASSWORD,

        lower: (password) =>
            /[a-z]/.test(password)
                ? ''
                : AUTH_ERROR_MESSAGES.PASSWORD,

        number: (password) =>
            /\d/.test(password)
                ? ''
                : AUTH_ERROR_MESSAGES.PASSWORD,

        noSpaces: (password) =>
            !/\s/.test(password)
                ? ''
                : AUTH_ERROR_MESSAGES.PASSWORD,

        special: (password) =>
            /[!#$%]/.test(password)
                ? ''
                : AUTH_ERROR_MESSAGES.PASSWORD
    },
    newPassword: {
        length: (password) =>
            password.length >= FIELD_LENGTHS.PASSWORD_MIN
                ? ''
                : AUTH_ERROR_MESSAGES.PASSWORD,

        upper: (password) =>
            /[A-Z]/.test(password)
                ? ''
                : AUTH_ERROR_MESSAGES.PASSWORD,

        lower: (password) =>
            /[a-z]/.test(password)
                ? ''
                : AUTH_ERROR_MESSAGES.PASSWORD,

        number: (password) =>
            /\d/.test(password)
                ? ''
                : AUTH_ERROR_MESSAGES.PASSWORD,

        noSpaces: (password) =>
            !/\s/.test(password)
                ? ''
                : AUTH_ERROR_MESSAGES.PASSWORD,

        special: (password) =>
            /[!#$%]/.test(password)
                ? ''
                : AUTH_ERROR_MESSAGES.PASSWORD
    },
    country: {
        isValid: (value) => {
            if (value.length < FIELD_LENGTHS.COUNTRY_MIN)
                return ADDRESS_ERROR_MESSAGES.COUNTRY_TOO_SHORT;
            if (value.length > FIELD_LENGTHS.COUNTRY_MAX)
                return ADDRESS_ERROR_MESSAGES.COUNTRY_TOO_LONG;
            if (!/^[A-Za-z\s]+$/.test(value))
                return ADDRESS_ERROR_MESSAGES.COUNTRY_INVALID_CHARS;
            return '';
        }
    },
    city: {
        isValid: (value) => {
            if (value.length < FIELD_LENGTHS.CITY_MIN)
                return ADDRESS_ERROR_MESSAGES.CITY_TOO_SHORT;
            if (value.length > FIELD_LENGTHS.CITY_MAX)
                return ADDRESS_ERROR_MESSAGES.CITY_TOO_LONG;
            if (!/^[A-Za-z\s]+$/.test(value))
                return ADDRESS_ERROR_MESSAGES.CITY_INVALID_CHARS;
            return '';
        }
    },
    zipCode: {
        isValid: (value) => {
            if (value.length < FIELD_LENGTHS.ZIP_CODE_MIN)
                return ADDRESS_ERROR_MESSAGES.ZIP_CODE_TOO_SHORT;
            if (value.length > FIELD_LENGTHS.ZIP_CODE_MAX)
                return ADDRESS_ERROR_MESSAGES.ZIP_CODE_TOO_LONG;
            return '';
        }
    },
    streetAddress: {
        isValid: (value) => {
            if (value.length < FIELD_LENGTHS.STREET_ADDRESS_MIN)
                return ADDRESS_ERROR_MESSAGES.STREET_ADDRESS_TOO_SHORT;
            if (value.length > FIELD_LENGTHS.STREET_ADDRESS_MAX)
                return ADDRESS_ERROR_MESSAGES.STREET_ADDRESS_TOO_LONG;
            return '';
        }
    },
    apartment: {
        isValid: (value) => {
            if (
                value &&
                value.length > FIELD_LENGTHS.APARTMENT_MAX
            )
                return ADDRESS_ERROR_MESSAGES.APARTMENT_TOO_LONG;
            return '';
        }
    },

    // Payment validators
    cardNumber: {
        isValid: (value) => {
            if (!value || value.length === 0) return '';

            // Use our payment validation patterns for spaced format
            const isValid = Object.values(
                PAYMENT_CONSTANTS.CARD_PATTERNS
            ).some((pattern) => new RegExp(pattern).test(value));

            if (!isValid) {
                return PAYMENT_CONSTANTS.ERRORS.CARD_NUMBER;
            }

            return '';
        }
    },

    cardHolderName: {
        isValid: (value) => {
            if (!value || value.length === 0) return '';

            if (
                value.length < FIELD_LENGTHS.CARD_HOLDER_NAME_MIN
            ) {
                return PAYMENT_CONSTANTS.ERRORS.CARD_HOLDER;
            }

            if (
                value.length > FIELD_LENGTHS.CARD_HOLDER_NAME_MAX
            ) {
                return PAYMENT_CONSTANTS.ERRORS.CARD_HOLDER;
            }

            if (
                !new RegExp(
                    PAYMENT_CONSTANTS.CARD_HOLDER_PATTERN
                ).test(value)
            ) {
                return PAYMENT_CONSTANTS.ERRORS.CARD_HOLDER;
            }

            return '';
        }
    },

    expiryDate: {
        isValid: (value) => {
            if (!value || value.length === 0) return '';

            // Check format (MM/YY)
            if (
                !new RegExp(
                    PAYMENT_CONSTANTS.EXPIRY_DATE_PATTERN
                ).test(value)
            ) {
                return PAYMENT_CONSTANTS.ERRORS.EXPIRY_DATE;
            }

            // Extract month and year
            const [month, year] = value.split('/');
            const monthNum = parseInt(month, 10);
            const yearNum = parseInt(`20${year}`, 10); // Convert YY to 20YY

            // Check if date is in the past
            const currentDate = new Date();
            const currentYear = currentDate.getFullYear();
            const currentMonth = currentDate.getMonth() + 1; // getMonth() is 0-indexed

            if (
                yearNum < currentYear ||
                (yearNum === currentYear &&
                    monthNum < currentMonth)
            ) {
                return PAYMENT_CONSTANTS.ERRORS.EXPIRED_CARD;
            }

            // Check if year is too far in the future (max 15 years)
            if (yearNum > currentYear + 15) {
                return PAYMENT_CONSTANTS.ERRORS.EXPIRY_DATE;
            }

            return '';
        }
    },

    cvv: {
        isValid: (value) => {
            if (!value || value.length === 0) return '';

            if (
                !new RegExp(PAYMENT_CONSTANTS.CVV_PATTERN).test(
                    value
                )
            ) {
                return PAYMENT_CONSTANTS.ERRORS.CVV;
            }

            return '';
        }
    }
};

export const getFormFieldErrorMessage = (field, value) => {
    const emptyErrorMessage = 'This field is required';
    const optionalFields = ['apartment'];

    if (value === '') {
        if (optionalFields.includes(field)) {
            return '';
        }
        return emptyErrorMessage;
    }

    if (!validators[field]) {
        return '';
    }

    let error = '';

    for (const validationFn of Object.values(validators[field])) {
        error = validationFn(value);

        if (error !== '') {
            return error;
        }
    }

    return error;
};
