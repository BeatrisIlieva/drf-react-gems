import { Fragment } from 'react';
import { InputField } from '../reusable/input-field/InputField';

export const FormFieldRenderer = ({
    fieldNames,
    formData,
    getInputClassName,
    handleFieldChange,
    validateField,
    registerInput,
    fieldConfig = {}
}) => {
    return fieldNames.map((fieldName) => {
        const fieldData = formData[fieldName];
        const config = fieldConfig[fieldName] || {};
        
        if (!fieldData) return null;

        return (
            <Fragment key={fieldName}>
                <InputField
                    getInputClassName={getInputClassName}
                    fieldData={fieldData}
                    handleFieldChange={handleFieldChange}
                    validateField={validateField}
                    fieldName={fieldName}
                    type={config.type || 'text'}
                    registerInput={registerInput}
                />
            </Fragment>
        );
    });
};
