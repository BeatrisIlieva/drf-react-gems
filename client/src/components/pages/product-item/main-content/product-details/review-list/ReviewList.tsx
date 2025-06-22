import type { ReactElement } from 'react';
import type { Params } from './types';
import { Stars } from '../../../../../reusable/stars/Stars';

import styles from './ReviewList.module.scss';
import { ReviewItem } from './review-item/ReviewItem';

export const ReviewList = ({
    averageRating,
    reviews
}: Params): ReactElement => {
    return (
        <section className={styles['reviews']}>
            <div className={styles['wrapper-top']}>
                <div>
                    <h3>Latest Customer Reviews</h3>
                    <div>
                        <span>{averageRating}</span>
                        <Stars rating={averageRating} />
                    </div>
                    <p>Average rating of all time</p>
                </div>
            </div>
            <ul>
                {reviews.map((review) => (
                    <ReviewItem key={review.id} review={review} />
                ))}
            </ul>
        </section>
    );
};
