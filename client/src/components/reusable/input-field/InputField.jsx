import { useEffect, useRef, useState } from 'react';

import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import { getDefaultMaxLength } from '../../../utils/formHelpers';
import { getFieldDisplayName } from '../../../utils/getFieldDisplayName';

import styles from './InputField.module.scss';

export const InputField = ({
    getInputClassName,
    fieldData,
    validateField,
    handleFieldChange,
    handleBlur,
    fieldName,
    type,
    registerInput,
    required,
    fieldConfig,
}) => {
    const onChangeHandler = handleFieldChange || validateField;

    const onBlurHandler = handleBlur || validateField;

    const fieldType = type || fieldConfig?.[fieldName]?.type || 'text';

    const maxLength =
        fieldData?.maxLength ||
        fieldConfig?.[fieldName]?.maxLength ||
        getDefaultMaxLength(fieldName, fieldType);

    const [isPasswordVisible, setIsPasswordVisible] = useState(false);
    const inputRef = useRef(null);

    useEffect(() => {
        if (registerInput && fieldName) {
            registerInput(fieldName, inputRef.current);
        }
        return () => {
            if (registerInput && fieldName) {
                registerInput(fieldName, null);
            }
        };
    }, [registerInput, fieldName]);

    return (
        <div className="field">
            <input
                ref={inputRef}
                className={getInputClassName(fieldData)}
                type={
                    fieldType === 'password' ? (isPasswordVisible ? 'text' : 'password') : fieldType
                }
                name={fieldName}
                id={fieldName}
                placeholder={fieldName}
                value={fieldData.value}
                onChange={onChangeHandler}
                onBlur={onBlurHandler}
                required={required}
                maxLength={maxLength}
            />
            <label htmlFor={fieldName} className={getInputClassName(fieldData)}>
                {fieldName === 'apartment'
                    ? getFieldDisplayName(fieldName)
                    : `${getFieldDisplayName(fieldName)}*`}
            </label>
            {fieldType === 'password' && (
                <FontAwesomeIcon
                    icon={isPasswordVisible ? faEyeSlash : faEye}
                    className={styles['eye-icon']}
                    onClick={() => setIsPasswordVisible(prev => !prev)}
                />
            )}
            {fieldData.error && <span className="error">{fieldData.error}</span>}
        </div>
    );
};
