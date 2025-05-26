import { Stars } from '../stars/Stars';
import styles from './ReviewItem.module.css';

export const ReviewItem = ({ review }) => {
    return (
        <li className={styles['review-item']}>
            <span>
                <span>
                    <img src={review.photo_url} alt={`${review.user_full_name}`} />
                </span>

                <span>
                    <h5>{review.user_full_name}</h5>
                    <Stars rating={review.rating} />
                    <span>{review.created_at.slice(0, 10)}</span>
                </span>
            </span>
            <span>{review.comment}</span>
        </li>
    );
};
