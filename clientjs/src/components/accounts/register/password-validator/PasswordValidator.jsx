import React, { useState } from 'react';
import styles from './PasswordValidator.module.css';

export const PasswordValidator = ({ password }) => {
    const [agree, setAgree] = useState(true);

    const validations = {
        length: password.length >= 8,
        upper: /[A-Z]/.test(password),
        lower: /[a-z]/.test(password),
        number: /\d/.test(password),
        noSpaces: !/\s/.test(password),
        special: /[!#$%]/.test(password)
    };

    const criteria = [
        { label: 'Must be at least 6 characters in length', key: 'length' },
        { label: 'Must contain at least one upper case letter', key: 'upper' },
        { label: 'Must contain at least one lower case letter', key: 'lower' },
        { label: 'Must contain at least one number', key: 'number' },
        { label: 'Must not contain spaces', key: 'noSpaces' },
        {
            label: 'Must contain at least one special character (!#$%)',
            key: 'special'
        }
    ];

    const showValidation = password.length > 0;

    return (
        <div className={styles['password-validator']}>
            <ul
                className={styles['password-validation-scale']}
                style={{ display: showValidation ? 'flex' : 'none' }}
            >
                {criteria.map(({ key }, index) => (
                    <li
                        key={index}
                        className={validations[key] ? styles.valid : ''}
                    />
                ))}
            </ul>

            <ul
                className={styles['password-criteria']}
                style={{ display: showValidation ? 'flex' : 'none' }}
            >
                {criteria.map(({ label, key }) => (
                    <li
                        key={key}
                        className={validations[key] ? styles.valid : ''}
                    >
                        {label}
                    </li>
                ))}
            </ul>

            <div className={styles['terms-wrapper']}>
                <input
                    type='checkbox'
                    name='agree'
                    id='agree'
                    required
                    checked={agree}
                    onChange={() => setAgree(!agree)}
                />
                <label className={styles['agree']}>
                    By creating an account, you agree to receive email updates
                </label>
            </div>
        </div>
    );
};
