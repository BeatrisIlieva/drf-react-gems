import { Stars } from '../../../../../../reusable/stars/Stars';

import styles from './ReviewItem.module.scss';

export const ReviewItem = ({ review }) => {
    return (
        <li className={styles['review-item']}>
            <span>
                <span>
                    <img src={review.photoUrl} alt={`${review.userFullName}`} />
                </span>

                <span>
                    <h5>{review.userFullName}</h5>
                    <Stars rating={review.rating} />
                    <span>{review.createdAt.slice(0, 10)}</span>
                </span>
            </span>
            <span>{review.comment}</span>
        </li>
    );
};
