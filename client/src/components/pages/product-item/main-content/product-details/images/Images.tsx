import type { ReactElement } from 'react';
import type { Params } from './types';

import styles from './Images.module.scss';

export const Images = ({
    firstImage,
    secondImage
}: Params): ReactElement => {
    return (
        <section className={styles['images']}>
            <div className={styles['thumbnail']}>
                <img src={firstImage} alt='Product First Image' />
            </div>

            <div className={styles['thumbnail']}>
                <img
                    src={secondImage}
                    alt='Product Second Image'
                />
            </div>
        </section>
    );
};
