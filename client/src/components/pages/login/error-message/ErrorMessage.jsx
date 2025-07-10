import styles from './ErrorMessage.module.scss';

export const ErrorMessage = ({ show }) => {
    if (!show) return null;

    return (
        <div className={styles['invalid-username-password']}>
            <p>Your email/username or password is incorrect.</p>
        </div>
    );
};
