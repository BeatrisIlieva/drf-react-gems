import React from 'react';
import type { FormFieldState } from '../../../types/User';
import { getFieldDisplayName } from '../../../utils/getFieldDisplayName';

interface InputFieldProps {
    getInputClassName: (fieldData: FormFieldState) => string;
    fieldData: FormFieldState;
    validateField?: (
        e: React.ChangeEvent<HTMLInputElement> | React.FocusEvent<HTMLInputElement>
    ) => void;
    handleFieldChange?: (
        e: React.ChangeEvent<HTMLInputElement>
    ) => void;
    handleBlur?: (e: React.FocusEvent<HTMLInputElement>) => void;
    fieldName: string;
    type: string;
}

export const InputField: React.FC<InputFieldProps> = ({
    getInputClassName,
    fieldData,
    validateField,
    handleFieldChange,
    handleBlur,
    fieldName,
    type
}) => {
    // Always use handleFieldChange for onChange to validate in real-time while typing
    // This ensures fields turn green as soon as they're valid
    const onChangeHandler = handleFieldChange || validateField;
    
    // On blur, always use validateField to show validation errors
    // This ensures errors only show when field loses focus
    const onBlurHandler = handleBlur || validateField;

    return (
        <div className='field'>
            <input
                className={getInputClassName(fieldData)}
                type={type}
                name={fieldName}
                id={fieldName}
                placeholder={fieldName}
                value={fieldData.value}
                onChange={onChangeHandler}
                onBlur={onBlurHandler}
            />
            <label
                htmlFor={fieldName}
                className={getInputClassName(fieldData)}
            >
                {`${getFieldDisplayName(fieldName)}*`}
            </label>
            {fieldData.error && (
                <span className='error'>{fieldData.error}</span>
            )}
        </div>
    );
};
