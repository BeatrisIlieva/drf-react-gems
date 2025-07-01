import styles from './Skeleton.module.scss';

export const Skeleton = () => {
    return (
        <div className={styles['skeleton-container']}>
            <div className={styles['skeleton-title']}></div>

            {Array.from({ length: 4 }).map((_, index) => (
                <div
                    key={index}
                    className={styles['skeleton-row']}
                >
                    <div
                        className={`${styles['skeleton-text']} ${styles['left']}`}
                    ></div>
                    <div
                        className={`${styles['skeleton-text']} ${styles['right']}`}
                    ></div>
                </div>
            ))}
        </div>
    );
};
