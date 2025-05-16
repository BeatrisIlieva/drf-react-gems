const passwordErrorMessage =
    'Sorry, the provided password does not match the required constraints';

const emailErrorMessage = 'Please enter a valid email address';

export const validators = {
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
            /[!#$%]/.test(password) ? '' : passwordErrorMessage
    }
};

export const getFormFieldErrorMessage = (field, value) => {
    const emptyErrorMessage = 'This field is required';

    if (value === '') {
        return emptyErrorMessage;
    }

    let error;

    for (const validationFn of Object.values(validators[field])) {
        error = validationFn(value);

        if (error !== '') {
            return error;
        }
    }

    return error;
};
