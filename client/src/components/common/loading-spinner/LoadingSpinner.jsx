import styles from './LoadingSpinner.module.scss';

export const LoadingSpinner = () => {
    return (
        <div className={styles['loading-spinner']}>
            <div className={styles['thumbnail']}>
                <img src="/logo.webp" alt="loading-spinner" />
            </div>
            <p>Loading...</p>
        </div>
    );
};
