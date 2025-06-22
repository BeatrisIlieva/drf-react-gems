import type { ReactElement } from 'react';

import styles from './ProductDetails.module.scss';
import { Images } from './images/Images';
import { ReviewList } from './review-list/ReviewList';

export const ProductDetails = (): ReactElement => {
    return (
        <section className={styles['product-details']}>
            <Images />
            <ReviewList />
        </section>
    );
};
