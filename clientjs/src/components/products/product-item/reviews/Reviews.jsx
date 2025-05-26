import { ReviewItem } from './review-item/ReviewItem';
import styles from './Reviews.module.css';
import { Stars } from './stars/Stars';

export const Reviews = ({ reviews, average_rating }) => {
    return (
        <section className={styles['reviews']}>
            <div className={styles['wrapper-top']}>
                <div>
                    <h3>Customer Reviews</h3>
                    <div>
                        <span>{average_rating}</span>
                        <Stars rating={average_rating} />
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
