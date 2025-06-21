import styles from './LoadingSpinner.module.scss';

export const LoadingSpinner = () => {
    return (
        <div className={styles['loading-spinner']}>
            <p>Loading</p>
        </div>
    )
}