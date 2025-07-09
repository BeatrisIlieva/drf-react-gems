import { createFormFieldConfig, getInitialFormValues } from '../utils/formHelpers';

import { FIELD_LENGTHS } from '../constants/fieldLengths';

const passwordUpdateFields = [
    {
        name: 'currentPassword',
        apiKey: 'current_password',
        required: true,
        label: 'Current Password',
        type: 'password',
        maxLength: FIELD_LENGTHS.PASSWORD_MAX,
    },
    {
        name: 'newPassword',
        apiKey: 'new_password',
        required: true,
        label: 'New Password',
        type: 'password',
        maxLength: FIELD_LENGTHS.PASSWORD_MAX,
    },
];

const loginFields = [
    {
        name: 'email_or_username',
        apiKey: 'email_or_username',
        required: true,
        label: 'Email or Username',
        maxLength: FIELD_LENGTHS.EMAIL_MAX,
    },
    {
        name: 'password',
        apiKey: 'password',
        required: true,
        label: 'Password',
        type: 'password',
        maxLength: FIELD_LENGTHS.PASSWORD_MAX,
    },
];

const registerFields = [
    {
        name: 'email',
        apiKey: 'email',
        required: true,
        label: 'Email',
        type: 'email',
        maxLength: FIELD_LENGTHS.EMAIL_MAX,
    },
    {
        name: 'username',
        apiKey: 'username',
        required: true,
        label: 'Username',
        maxLength: FIELD_LENGTHS.USERNAME_MAX,
    },
    {
        name: 'password',
        apiKey: 'password',
        required: true,
        label: 'Password',
        type: 'password',
        maxLength: FIELD_LENGTHS.PASSWORD_MAX,
    },
];

const deliveryAddressFields = [
    {
        name: 'firstName',
        apiKey: 'first_name',
        required: true,
        label: 'First Name',
        maxLength: FIELD_LENGTHS.FIRST_NAME_MAX,
    },
    {
        name: 'lastName',
        apiKey: 'last_name',
        required: true,
        label: 'Last Name',
        maxLength: FIELD_LENGTHS.LAST_NAME_MAX,
    },
    {
        name: 'phoneNumber',
        apiKey: 'phone_number',
        required: true,
        label: 'Phone Number',
        type: 'tel',
        maxLength: FIELD_LENGTHS.PHONE_NUMBER_MAX,
    },
    {
        name: 'country',
        apiKey: 'country',
        required: true,
        label: 'Country',
        maxLength: FIELD_LENGTHS.COUNTRY_MAX,
    },
    {
        name: 'city',
        apiKey: 'city',
        required: true,
        label: 'City',
        maxLength: FIELD_LENGTHS.CITY_MAX,
    },
    {
        name: 'zipCode',
        apiKey: 'zip_code',
        required: true,
        label: 'ZIP Code',
        maxLength: FIELD_LENGTHS.ZIP_CODE_MAX,
    },
    {
        name: 'streetAddress',
        apiKey: 'street_address',
        required: true,
        label: 'Street Address',
        maxLength: FIELD_LENGTHS.STREET_ADDRESS_MAX,
    },
    {
        name: 'apartment',
        apiKey: 'apartment',
        required: false,
        label: 'Apartment (Optional)',
        maxLength: FIELD_LENGTHS.APARTMENT_MAX,
    },
];

const paymentFields = [
    {
        name: 'cardNumber',
        apiKey: 'card_number',
        required: true,
        label: 'Card Number',
        type: 'text',
        maxLength: FIELD_LENGTHS.CARD_NUMBER_MAX,
    },
    {
        name: 'cardHolderName',
        apiKey: 'card_holder_name',
        required: true,
        label: 'Name on card',
        type: 'text',
        maxLength: FIELD_LENGTHS.CARD_HOLDER_NAME_MAX,
    },
    {
        name: 'expiryDate',
        apiKey: 'expiry_date',
        required: true,
        label: 'MM/YY',
        type: 'text',
        maxLength: FIELD_LENGTHS.EXPIRY_DATE_MAX,
    },
    {
        name: 'cvv',
        apiKey: 'cvv',
        required: true,
        label: 'CVV',
        type: 'text',
        maxLength: FIELD_LENGTHS.CVV_MAX,
    },
];

export const FORM_CONFIGS = {
    passwordUpdate: {
        fieldConfig: createFormFieldConfig(passwordUpdateFields),
        get initialValues() {
            return getInitialFormValues(
                passwordUpdateFields.map(f => f.name),
                this.fieldConfig
            );
        },
        title: 'Change Password',
    },
    login: {
        fieldConfig: createFormFieldConfig(loginFields),
        get initialValues() {
            return getInitialFormValues(
                loginFields.map(f => f.name),
                this.fieldConfig
            );
        },
        title: 'Login',
    },
    register: {
        fieldConfig: createFormFieldConfig(registerFields),
        get initialValues() {
            return getInitialFormValues(
                registerFields.map(f => f.name),
                this.fieldConfig
            );
        },
        title: 'Register',
    },
    deliveryAddress: {
        fieldConfig: createFormFieldConfig(deliveryAddressFields),
        get initialValues() {
            return getInitialFormValues(
                deliveryAddressFields.map(f => f.name),
                this.fieldConfig
            );
        },
        title: 'Delivery Information',
    },
    payment: {
        fieldConfig: createFormFieldConfig(paymentFields),
        get initialValues() {
            return getInitialFormValues(
                paymentFields.map(f => f.name),
                this.fieldConfig
            );
        },
        title: 'Payment',
    },
};
