import { Images } from './images/Images';
import { ReviewList } from './review-list/ReviewList';

import styles from './ProductDetails.module.scss';

export const ProductDetails = () => {
    return (
        <section className={styles['product-details']}>
            <Images />
            <ReviewList />
        </section>
    );
};
