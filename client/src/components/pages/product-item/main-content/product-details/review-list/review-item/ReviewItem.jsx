import { useState } from 'react';

import { Stars } from '../../../../../../reusable/stars/Stars';

import { useReviewApi } from '../../../../../../../api/reviewApi';

import { useAuth } from '../../../../../../../hooks/useAuth';

import styles from './ReviewItem.module.scss';

export const ReviewItem = ({ review, onReviewUpdated }) => {
    const { permissions } = useAuth();
    const { approveReview, unapproveReview } = useReviewApi();
    const [isUpdating, setIsUpdating] = useState(false);

    const isReviewer = permissions?.includes('products.approve_review');

    const handleApproveReview = async () => {
        if (!isReviewer || isUpdating) return;

        setIsUpdating(true);
        try {
            await approveReview(review.id);

            if (onReviewUpdated) {
                onReviewUpdated();
            }
        } catch (error) {
            console.error('Error approving review:', error);
        } finally {
            setIsUpdating(false);
        }
    };

    const handleUnapproveReview = async () => {
        if (!isReviewer || isUpdating) return;

        setIsUpdating(true);
        try {
            await unapproveReview(review.id);

            if (onReviewUpdated) {
                onReviewUpdated();
            }
        } catch (error) {
            console.error('Error unapproving review:', error);
        } finally {
            setIsUpdating(false);
        }
    };

    return (
        <li className={styles['review-item']}>
            <span>
                <span>
                    {review.photoUrl ? (
                        <img src={review.photoUrl} alt={`${review.userFullName}`} />
                    ) : (
                        <img
                            src="https://res.cloudinary.com/dpgvbozrb/image/upload/v1750959197/user-1699635_1280_z3dgxn.png"
                            alt="Profile"
                            className={styles['profile-photo']}
                        />
                    )}
                </span>

                <span>
                    <h5>{review.userFullName}</h5>
                    <Stars rating={review.rating} fontSize={0.9} />
                    <span>{review.createdAt.slice(0, 10)}</span>
                </span>
            </span>
            <span>{review.comment}</span>

            {isReviewer && (
                <div className={styles['approval-controls']}>
                    {review.approved ? (
                        <button
                            onClick={handleUnapproveReview}
                            disabled={isUpdating}
                            className={`${styles['approval-btn']} ${styles['unapprove-btn']}`}
                        >
                            {isUpdating ? 'Unapproving...' : 'Unapprove'}
                        </button>
                    ) : (
                        <button
                            onClick={handleApproveReview}
                            disabled={isUpdating}
                            className={`${styles['approval-btn']} ${styles['approve-btn']}`}
                        >
                            {isUpdating ? 'Approving...' : 'Approve'}
                        </button>
                    )}
                </div>
            )}
        </li>
    );
};
