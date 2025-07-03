import { useState, useRef, useEffect } from 'react';
import { getFieldDisplayName } from '../../../utils/getFieldDisplayName';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
    faEye,
    faEyeSlash
} from '@fortawesome/free-solid-svg-icons';
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
    required
}) => {
    const onChangeHandler = handleFieldChange || validateField;

    const onBlurHandler = handleBlur || validateField;

    const [isPasswordVisible, setIsPasswordVisible] =
        useState(false);
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
        <div className='field'>
            <input
                ref={inputRef}
                className={getInputClassName(fieldData)}
                type={
                    type === 'password'
                        ? isPasswordVisible
                            ? 'text'
                            : 'password'
                        : type
                }
                name={fieldName}
                id={fieldName}
                placeholder={fieldName}
                value={fieldData.value}
                onChange={onChangeHandler}
                onBlur={onBlurHandler}
                required={required}
            />
            <label
                htmlFor={fieldName}
                className={getInputClassName(fieldData)}
            >
                {fieldName === 'apartment'
                    ? getFieldDisplayName(fieldName)
                    : `${getFieldDisplayName(fieldName)}*`}
            </label>
            {type === 'password' && (
                <FontAwesomeIcon
                    icon={isPasswordVisible ? faEyeSlash : faEye}
                    className={styles['eye-icon']}
                    onClick={() =>
                        setIsPasswordVisible((prev) => !prev)
                    }
                />
            )}
            {fieldData.error && (
                <span className='error'>{fieldData.error}</span>
            )}
        </div>
    );
};
