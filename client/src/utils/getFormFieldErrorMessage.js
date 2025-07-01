const passwordErrorMessage =
    'Sorry, the provided password does not match the required constraints';

const emailErrorMessage = 'Please enter a valid email address';
const usernameErrorMessage =
    'Username must be 3-30 characters long and contain only letters, numbers, and underscores';
const nameErrorMessage =
    'Name must contain only letters and be 2-30 characters long';
const phoneErrorMessage = 'Phone number must be 9-15 digits long';
const emailOrUsernameErrorMessage =
    'Please enter a valid email address or username';

export const validators = {
    email: {
        isValid: (value) =>
            /^[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/i.test(
                value
            )
                ? ''
                : emailErrorMessage
    },
    username: {
        isValid: (value) =>
            /^[A-Za-z0-9_]{3,30}$/.test(value)
                ? ''
                : usernameErrorMessage
    },
    email_or_username: {
        isValid: (value) => {
            const isEmail =
                /^[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/i.test(
                    value
                );
            const isUsername = /^[A-Za-z0-9_]{3,30}$/.test(value);

            return isEmail || isUsername
                ? ''
                : emailOrUsernameErrorMessage;
        }
    },
    password: {
        length: (password) =>
            password.length >= 6 ? '' : passwordErrorMessage,

        upper: (password) =>
            /[A-Z]/.test(password) ? '' : passwordErrorMessage,

        lower: (password) =>
            /[a-z]/.test(password) ? '' : passwordErrorMessage,

        number: (password) =>
            /\d/.test(password) ? '' : passwordErrorMessage,

        noSpaces: (password) =>
            !/\s/.test(password) ? '' : passwordErrorMessage,

        special: (password) =>
            /[!#$%]/.test(password) ? '' : passwordErrorMessage
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
    },
    currentPassword: {
        length: (password) =>
            password.length >= 6 ? '' : passwordErrorMessage,

        upper: (password) =>
            /[A-Z]/.test(password) ? '' : passwordErrorMessage,

        lower: (password) =>
            /[a-z]/.test(password) ? '' : passwordErrorMessage,

        number: (password) =>
            /\d/.test(password) ? '' : passwordErrorMessage,

        noSpaces: (password) =>
            !/\s/.test(password) ? '' : passwordErrorMessage,

        special: (password) =>
            /[!#$%]/.test(password) ? '' : passwordErrorMessage
    },
    newPassword: {
        length: (password) =>
            password.length >= 6 ? '' : passwordErrorMessage,

        upper: (password) =>
            /[A-Z]/.test(password) ? '' : passwordErrorMessage,

        lower: (password) =>
            /[a-z]/.test(password) ? '' : passwordErrorMessage,

        number: (password) =>
            /\d/.test(password) ? '' : passwordErrorMessage,

        noSpaces: (password) =>
            !/\s/.test(password) ? '' : passwordErrorMessage,

        special: (password) =>
            /[!#$%]/.test(password) ? '' : passwordErrorMessage
    }
};

export const getFormFieldErrorMessage = (field, value) => {
    const emptyErrorMessage = 'This field is required';

    if (value === '') {
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
