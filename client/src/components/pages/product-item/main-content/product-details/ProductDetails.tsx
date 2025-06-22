import type { ReactElement } from 'react';
import type { Params } from './types';

import styles from './ProductDetails.module.scss';
import { Images } from './images/Images';

export const ProductDetails = ({
    firstImage,
    secondImage,
    averageRating,
    reviews
}: Params): ReactElement => {
    return (
        <section className={styles['product-details']}>
            <Images
                firstImage={firstImage}
                secondImage={secondImage}
            />
        </section>
    );
};
