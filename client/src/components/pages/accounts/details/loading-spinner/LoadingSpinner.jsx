import styles from './LoadingSpinner.module.scss';

export const LoadingSpinner = ({
    size = 'medium',
    message = 'Loading...'
}) => {
    return (
        <div className={styles['loading-container']}>
            <div
                className={`${styles['spinner']} ${styles[size]}`}
            />
            {message && (
                <p className={styles['loading-text']}>
                    {message}
                </p>
            )}
        </div>
    );
};
