import type { ReactElement } from 'react';

import styles from './Skeleton.module.scss';

export const Skeleton = (): ReactElement => {
    return (
        <div className={styles['loading-container']}>
            <div className={styles['skeleton-grid']}>
                {Array.from({ length: 12 }).map((_, index) => (
                    <div
                        key={index}
                        className={styles['skeleton-card']}
                    >
                        <div
                            className={styles['skeleton-image']}
                        ></div>
                        <div
                            className={styles['skeleton-text']}
                        ></div>
                        <div
                            className={
                                styles['skeleton-text-short']
                            }
                        ></div>
                    </div>
                ))}
            </div>
        </div>
    );
};
