import { PRODUCTS_PER_PAGE } from '../../../../constants/pagination';

import styles from './Skeleton.module.scss';

export const Skeleton = () => {
    return (
        <div className={styles['loading-container']}>
            <div className={styles['skeleton-grid']}>
                {Array.from({ length: PRODUCTS_PER_PAGE }).map(
                    (_, index) => (
                        <div
                            key={index}
                            className={styles['skeleton-card']}
                        >
                            <div
                                className={
                                    styles['skeleton-image']
                                }
                            ></div>
                            <div
                                className={
                                    styles['skeleton-text']
                                }
                            ></div>
                            <div
                                className={
                                    styles['skeleton-text-short']
                                }
                            ></div>
                        </div>
                    )
                )}
            </div>
        </div>
    );
};
