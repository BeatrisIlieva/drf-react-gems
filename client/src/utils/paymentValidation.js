import { PAYMENT_CONSTANTS } from '../constants/paymentConstants';

export const validatePaymentField = (fieldName, value) => {
    const errors = {};

    switch (fieldName) {
        case 'cardNumber':
            if (!value) {
                errors[fieldName] = 'Card number is required';
            } else {
                const isValid = Object.values(
                    PAYMENT_CONSTANTS.CARD_PATTERNS
                ).some((pattern) =>
                    new RegExp(pattern).test(value)
                );
                if (!isValid) {
                    errors[fieldName] =
                        PAYMENT_CONSTANTS.ERRORS.CARD_NUMBER;
                }
            }
            break;

        case 'cardHolderName':
            if (!value) {
                errors[fieldName] =
                    'Card holder name is required';
            } else if (
                !new RegExp(
                    PAYMENT_CONSTANTS.CARD_HOLDER_PATTERN
                ).test(value)
            ) {
                errors[fieldName] =
                    PAYMENT_CONSTANTS.ERRORS.CARD_HOLDER;
            }
            break;

        case 'cvv':
            if (!value) {
                errors[fieldName] = 'CVV is required';
            } else if (
                !new RegExp(PAYMENT_CONSTANTS.CVV_PATTERN).test(
                    value
                )
            ) {
                errors[fieldName] = PAYMENT_CONSTANTS.ERRORS.CVV;
            }
            break;

        case 'expiryDate':
            if (!value) {
                errors[fieldName] = 'Expiry date is required';
            } else {
                const expiryPattern = new RegExp(
                    PAYMENT_CONSTANTS.EXPIRY_DATE_PATTERN
                );
                if (!expiryPattern.test(value)) {
                    errors[fieldName] =
                        PAYMENT_CONSTANTS.ERRORS.EXPIRY_DATE;
                } else {
                    // Check if card is expired
                    const [month, year] = value.split('/');
                    const currentDate = new Date();
                    const currentYear =
                        currentDate.getFullYear() % 100;
                    const currentMonth =
                        currentDate.getMonth() + 1;

                    const expYear = parseInt(year, 10);
                    const expMonth = parseInt(month, 10);

                    if (
                        expYear < currentYear ||
                        (expYear === currentYear &&
                            expMonth < currentMonth)
                    ) {
                        errors[fieldName] =
                            PAYMENT_CONSTANTS.ERRORS.EXPIRED_CARD;
                    }
                }
            }
            break;

        default:
            break;
    }

    return errors;
};

export const validateAllPaymentFields = (formData) => {
    const errors = {};

    Object.keys(formData).forEach((fieldName) => {
        const fieldErrors = validatePaymentField(
            fieldName,
            formData[fieldName]
        );
        Object.assign(errors, fieldErrors);
    });

    return errors;
};

export const formatCardNumber = (value) => {
    // Remove all non-digit characters
    const digits = value.replace(/\D/g, '');

    // Add spaces every 4 digits
    const formatted = digits.replace(/(\d{4})(?=\d)/g, '$1 ');

    // Limit to 19 characters (16 digits + 3 spaces)
    return formatted.substring(0, 19);
};

export const formatExpiryDate = (value) => {
    // Remove all non-digit characters
    const digits = value.replace(/\D/g, '');

    // Add slash after 2 digits
    if (digits.length >= 2) {
        return `${digits.substring(0, 2)}/${digits.substring(
            2,
            4
        )}`;
    }

    return digits;
};

export const formatCvv = (value) => {
    // Remove all non-digit characters and limit to 3 digits
    return value.replace(/\D/g, '').substring(0, 3);
};
