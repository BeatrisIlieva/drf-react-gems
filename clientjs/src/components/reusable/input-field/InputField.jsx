import { useState } from 'react';

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
    fieldName,
    type
}) => {
    const [isPasswordVisible, setIsPasswordVisible] =
        useState(false);
    return (
        <div className='field'>
            <input
                className={getInputClassName(fieldData)}
                type={
                    type === 'text' || !isPasswordVisible
                        ? type
                        : 'password'
                }
                name={fieldName}
                id={fieldName}
                placeholder={fieldName}
                value={fieldData.value}
                onChange={validateField}
                onBlur={validateField}
            />
            <label
                htmlFor={fieldName}
                className={getInputClassName(fieldData)}
            >
                {`${
                    fieldName.charAt(0).toUpperCase() +
                    fieldName.slice(1)
                }*`}
            </label>
            <i
                onClick={setIsPasswordVisible((prev) => !prev)}
                className={
                    isPasswordVisible ? (
                        <FontAwesomeIcon
                            icon={faEyeSlash}
                            className={styles['eye-icon']}
                        />
                    ) : (
                        <FontAwesomeIcon
                            icon={faEye}
                            className={styles['eye-icon']}
                        />
                    )
                }
            ></i>
            {fieldData.error && (
                <span className='error'>{fieldData.error}</span>
            )}
        </div>
    );
};
