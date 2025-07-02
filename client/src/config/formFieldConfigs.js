import { createFormFieldConfig, getInitialFormValues } from '../utils/formHelpers';

const personalInfoFields = [
    {
        name: 'firstName',
        apiKey: 'first_name',
        required: true,
        label: 'First Name'
    },
    {
        name: 'lastName', 
        apiKey: 'last_name',
        required: true,
        label: 'Last Name'
    },
    {
        name: 'phoneNumber',
        apiKey: 'phone_number', 
        required: true,
        label: 'Phone Number',
        type: 'tel'
    }
];

const deliveryAddressFields = [
    {
        name: 'state',
        apiKey: 'state',
        required: true,
        label: 'State',
        type: 'select'
    },
    {
        name: 'city',
        apiKey: 'city',
        required: true,
        label: 'City',
        type: 'select'
    },
    {
        name: 'zipCode',
        apiKey: 'zip_code',
        required: true,
        label: 'ZIP Code',
        type: 'select'
    },
    {
        name: 'streetAddress',
        apiKey: 'street_address',
        required: true,
        label: 'Street Address',
        type: 'select'
    },
    {
        name: 'apartment',
        apiKey: 'apartment',
        required: false,
        label: 'Apartment/Unit'
    }
];

const paymentCardFields = [
    {
        name: 'cardNumber',
        apiKey: 'card_number',
        required: true,
        label: 'Card Number'
    },
    {
        name: 'expiryDate',
        apiKey: 'expiry_date',
        required: true,
        label: 'Expiry Date'
    },
    {
        name: 'cvv',
        apiKey: 'cvv',
        required: true,
        label: 'CVV'
    },
    {
        name: 'cardHolderName',
        apiKey: 'card_holder_name',
        required: true,
        label: 'Cardholder Name'
    }
];

export const FORM_CONFIGS = {
    personalInfo: {
        fieldConfig: createFormFieldConfig(personalInfoFields),
        initialValues: getInitialFormValues(personalInfoFields.map(f => f.name)),
        title: 'Personal Information'
    },
    deliveryAddress: {
        fieldConfig: createFormFieldConfig(deliveryAddressFields),
        initialValues: getInitialFormValues(deliveryAddressFields.map(f => f.name)),
        title: 'Delivery Information'
    },
    paymentCard: {
        fieldConfig: createFormFieldConfig(paymentCardFields),
        initialValues: getInitialFormValues(paymentCardFields.map(f => f.name)),
        title: 'Payment Information'
    }
};
