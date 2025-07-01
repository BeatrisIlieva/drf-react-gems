import styles from './PasswordValidator.module.scss';

export const PasswordValidator = ({ password }) => {
    const validations = {
        length: password.length >= 6,
        upper: /[A-Z]/.test(password),
        lower: /[a-z]/.test(password),
        number: /\d/.test(password),
        noSpaces: !/\s/.test(password),
        special: /[!#$%]/.test(password)
    };

    const criteria = [
        {
            label: 'Must be at least 6 characters in length',
            key: 'length'
        },
        {
            label: 'Must contain at least one upper case letter',
            key: 'upper'
        },
        {
            label: 'Must contain at least one lower case letter',
            key: 'lower'
        },
        {
            label: 'Must contain at least one number',
            key: 'number'
        },
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
                style={{
                    display: showValidation ? 'flex' : 'none'
                }}
            >
                {criteria.map(({ key }, index) => (
                    <li
                        key={index}
                        className={
                            validations[key] ? styles.valid : ''
                        }
                    />
                ))}
            </ul>

            <ul
                className={styles['password-criteria']}
                style={{
                    display: showValidation ? 'flex' : 'none'
                }}
            >
                {criteria.map(({ label, key }) => (
                    <li
                        key={key}
                        className={
                            validations[key] ? styles.valid : ''
                        }
                    >
                        {label}
                    </li>
                ))}
            </ul>
        </div>
    );
};
