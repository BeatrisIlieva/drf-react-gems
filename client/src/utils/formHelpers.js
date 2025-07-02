export const createFormFieldConfig = (fields) => {
    return fields.reduce((config, field) => {
        config[field.name] = {
            name: field.name,
            apiKey: field.apiKey || field.name,
            required: field.required !== false,
            type: field.type || 'text',
            label: field.label,
            validation: field.validation || []
        };
        return config;
    }, {});
};

export const getInitialFormValues = (fieldNames) => {
    return fieldNames.reduce((values, fieldName) => {
        values[fieldName] = { value: '', error: '', valid: false };
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
