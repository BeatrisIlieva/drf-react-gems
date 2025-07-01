import React, { useState } from 'react';
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
    type
}) => {
    const onChangeHandler = handleFieldChange || validateField;

    const onBlurHandler = handleBlur || validateField;

    const [isPasswordVisible, setIsPasswordVisible] = useState(false);

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
