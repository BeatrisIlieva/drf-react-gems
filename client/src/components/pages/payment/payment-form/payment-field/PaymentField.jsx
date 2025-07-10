import { CardNumberInput } from '../../../../reusable/card-number-input/CardNumberInput';
import { InputField } from '../../../../reusable/input-field/InputField';

export const PaymentField = ({
    fieldName,
    fieldData,
    fieldConfig,
    handleFormattedFieldChange,
    validateField,
    registerInput,
    getInputClassName,
}) => {
    if (!fieldData) return null;

    const config = fieldConfig[fieldName] || {};

    if (fieldName === 'cardNumber') {
        return (
            <CardNumberInput
                fieldName={fieldName}
                fieldData={fieldData}
                handleFieldChange={handleFormattedFieldChange}
                validateField={validateField}
                registerInput={registerInput}
                fieldConfig={fieldConfig}
                getInputClassName={getInputClassName}
            />
        );
    }

    return (
        <InputField
            getInputClassName={getInputClassName}
            fieldData={fieldData}
            handleFieldChange={handleFormattedFieldChange}
            validateField={validateField}
            fieldName={fieldName}
            type={config.type || 'text'}
            registerInput={registerInput}
            fieldConfig={fieldConfig}
        />
    );
};
