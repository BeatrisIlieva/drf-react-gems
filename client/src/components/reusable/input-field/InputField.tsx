import React, { useState } from 'react';
import type { FormFieldState } from '../../../types/User';
import { getFieldDisplayName } from '../../../utils/getFieldDisplayName';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
    faEye,
    faEyeSlash
} from '@fortawesome/free-solid-svg-icons';
import styles from './InputField.module.scss';

interface InputFieldProps {
    getInputClassName: (fieldData: FormFieldState) => string;
    fieldData: FormFieldState;
    validateField?: (
        e:
            | React.ChangeEvent<HTMLInputElement>
            | React.FocusEvent<HTMLInputElement>
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
    const onChangeHandler = handleFieldChange || validateField;

    const onBlurHandler = handleBlur || validateField;

    const [isPasswordVisible, setIsPasswordVisible] =
        useState<boolean>(false);

    return (
        <>
            <div className='field'>
                <input
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
                />
                <label
                    htmlFor={fieldName}
                    className={getInputClassName(fieldData)}
                >
                    {`${getFieldDisplayName(fieldName)}*`}
                </label>

                {type === 'password' && (
                    <FontAwesomeIcon
                        icon={
                            isPasswordVisible ? faEyeSlash : faEye
                        }
                        className={styles['eye-icon']}
                        onClick={() =>
                            setIsPasswordVisible((prev) => !prev)
                        }
                    />
                )}
            </div>
            {fieldData.error && (
                <span className='error'>{fieldData.error}</span>
            )}
        </>
    );
};
