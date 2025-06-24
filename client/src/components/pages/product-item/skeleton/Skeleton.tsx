import styles from './Skeleton.module.scss';

export const Skeleton = () => {
    return (
        <div className={styles['product-item-loader']}>
            <div className={styles['product-skeleton']}>
                <div className={styles['skeleton-nav']}></div>

                <div className={styles['skeleton-content']}>
                    <div className={styles['skeleton-images']}>
                        <div
                            className={
                                styles['skeleton-main-image']
                            }
                        ></div>
                        <div
                            className={
                                styles[
                                    'skeleton-thumbnail-container'
                                ]
                            }
                        >
                            {Array.from({
                                length: 3
                            }).map((_, i) => (
                                <div
                                    key={i}
                                    className={
                                        styles[
                                            'skeleton-thumbnail'
                                        ]
                                    }
                                ></div>
                            ))}
                        </div>
                    </div>

                    <div className={styles['skeleton-details']}>
                        <div
                            className={styles['skeleton-title']}
                        ></div>
                        <div
                            className={styles['skeleton-text']}
                        ></div>
                        <div
                            className={styles['skeleton-price']}
                        ></div>
                        <div
                            className={styles['skeleton-options']}
                        ></div>
                        <div
                            className={styles['skeleton-button']}
                        ></div>
                    </div>
                </div>

                <div className={styles['skeleton-related']}></div>
            </div>
        </div>
    );
};
