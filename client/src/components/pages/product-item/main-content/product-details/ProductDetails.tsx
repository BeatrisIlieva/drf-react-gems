import type { ReactElement } from 'react';
import type { Params } from './types';

import styles from './ProductDetails.module.scss';
import { Images } from './images/Images';
import { ReviewList } from './review-list/ReviewList';

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
            <ReviewList
                averageRating={averageRating}
                reviews={reviews}
            />
        </section>
    );
};
