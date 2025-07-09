export const createFormFieldConfig = fields => {
    return fields.reduce((config, field) => {
        config[field.name] = {
            name: field.name,
            apiKey: field.apiKey || field.name,
            required: field.required !== false,
            type: field.type || 'text',
            label: field.label,
            validation: field.validation || [],
            maxLength: field.maxLength || getDefaultMaxLength(field.name, field.type),
        };
        return config;
    }, {});
};

export const getInitialFormValues = (fieldNames, fieldConfig = {}) => {
    return fieldNames.reduce((values, fieldName) => {
        const config = fieldConfig[fieldName] || {};
        values[fieldName] = {
            value: '',
            error: '',
            valid: false,
            maxLength: config.maxLength,
        };
        return values;
    }, {});
};

export const createApiDataFromForm = (formData, fieldConfig) => {
    const apiData = {};
    Object.keys(formData).forEach(fieldName => {
        const field = fieldConfig[fieldName];
        const value = formData[fieldName]?.value?.trim();
        if (value && field) {
            apiData[field.apiKey] = value;
        }
    });
    return apiData;
};

export const getDefaultMaxLength = (fieldName, fieldType) => {
    const defaultLengths = {
        email: 254,
        email_or_username: 254,
        username: 30,
        firstName: 30,
        lastName: 30,
        phoneNumber: 15,
        password: 128,
        currentPassword: 128,
        newPassword: 128,
        streetAddress: 100,
        apartment: 50,
        city: 50,
        state: 50,
        zipCode: 10,
        cardNumber: 19,
        cardHolderName: 50,
        cvv: 4,
    };

    if (fieldType === 'password') return 128;
    if (fieldType === 'email') return 254;
    if (fieldType === 'tel') return 15;

    return defaultLengths[fieldName] || 100;
};
