type ValidatorFn = (value: string) => string;

interface ValidatorType {
    [key: string]: {
        [key: string]: ValidatorFn;
    };
}

const passwordErrorMessage =
    'Sorry, the provided password does not match the required constraints';

const emailErrorMessage = 'Please enter a valid email address';
const nameErrorMessage = 'Name must contain only letters and be 2-30 characters long';
const phoneErrorMessage = 'Phone number must be 9-15 digits long';

export const validators: ValidatorType = {
    email: {
        isValid: (value) =>
            /^[A-Za-z0-9]+@+[a-z]+\.[a-z]{2,4}$/.test(value)
                ? ''
                : emailErrorMessage
    },
    password: {
        length: (password) =>
            password.length >= 6 ? '' : passwordErrorMessage,

        upper: (password) =>
            /[A-Z]/.test(password) ? '' : passwordErrorMessage,

        lower: (password) =>
            /[a-z]/.test(password) ? '' : passwordErrorMessage,

        number: (password) => (/\d/.test(password) ? '' : passwordErrorMessage),

        noSpaces: (password) =>
            !/\s/.test(password) ? '' : passwordErrorMessage,

        special: (password) =>
            /[!#$%]/.test(password) ? '' : passwordErrorMessage,
    },
    firstName: {
        isValid: (value) =>
            /^[A-Za-z]{2,30}$/.test(value) ? '' : nameErrorMessage
    },
    lastName: {
        isValid: (value) =>
            /^[A-Za-z]{2,30}$/.test(value) ? '' : nameErrorMessage
    },
    phoneNumber: {
        isValid: (value) =>
            /^\d{9,15}$/.test(value) ? '' : phoneErrorMessage
    }
};

export const getFormFieldErrorMessage = (field: string, value: string): string => {
    const emptyErrorMessage = 'This field is required';

    if (value === '') {
        return emptyErrorMessage;
    }

    if (!validators[field]) {
        return '';  // If no validators for this field, consider valid
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
