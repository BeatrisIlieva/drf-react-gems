import { useEffect, useState } from 'react';

import { Button } from '../../../../../../reusable/button/Button';
import { DeleteButton } from '../../../../../../reusable/delete-button/DeleteButton';
import { Deletion } from '../../../../../../reusable/deletion/Deletion';
import { Popup } from '../../../../../../reusable/popup/Popup';
import { Stars } from '../../../../../../reusable/stars/Stars';

import { useReview } from '../../../../../../../api/reviewApi';

import { useAuth } from '../../../../../../../hooks/useAuth';

import styles from './ReviewForm.module.scss';

export const ReviewForm = ({
    productId,
    contentType,
    onReviewSubmitted = null,
    existingReview = null,
}) => {
    const [rating, setRating] = useState(existingReview?.rating || 0);
    const [comment, setComment] = useState(existingReview?.comment || '');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    const [isDeleteReviewPopupOpen, setIsDeleteReviewPopupOpen] = useState(false);

    const { createReview, updateReview, deleteReview } = useReview();
    const { isAuthenticated } = useAuth();

    useEffect(() => {
        if (existingReview) {
            setRating(existingReview.rating);
            setComment(existingReview.comment || '');
        } else {
            setRating(0);
            setComment('');
        }
    }, [existingReview]);

    const handleSubmit = async e => {
        e.preventDefault();

        setSuccess(false);

        if (rating === 0) {
            setError('Please select a rating');
            return;
        }

        if (!comment.trim()) {
            setError('Please write a comment');
            return;
        }

        setIsSubmitting(true);
        setError(null);

        try {
            const reviewData = {
                rating,
                comment: comment.trim(),
                contentType,
                objectId: productId,
            };

            let response;
            if (existingReview) {
                response = await updateReview(existingReview.id, reviewData);
            } else {
                response = await createReview(reviewData);
            }

            setSuccess(true);
            if (onReviewSubmitted) {
                onReviewSubmitted(response);
            }

            if (!existingReview) {
                setRating(0);
                setComment('');
            }

            setTimeout(() => setSuccess(false), 3000);
        } catch (err) {
            setError('Ensure this field has no more than 300 characters.');
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleRatingChange = newRating => {
        setRating(newRating);

        if (newRating > 0 && error === 'Please select a rating') {
            setError(null);
        }
    };

    const handleCommentChange = e => {
        setComment(e.target.value);

        if (e.target.value.trim() && error === 'Please write a comment') {
            setError(null);
        }
    };

    const handleDelete = async () => {
        if (!existingReview || !isAuthenticated) {
            return;
        }

        setIsDeleting(true);
        setError(null);
        setIsDeleteReviewPopupOpen(false);

        try {
            await deleteReview(existingReview.id);

            if (onReviewSubmitted) {
                onReviewSubmitted(null);
            }

            setTimeout(() => setSuccess(false), 3000);
        } catch (err) {
            setError(err.message || 'Failed to delete review');
        } finally {
            setIsDeleting(false);
        }
    };

    return (
        <>
            <div className={styles['review-form']}>
                <div className={styles['rate-header']}>
                    <h5>{existingReview ? 'Update your review' : 'Rate this product'}</h5>
                    <Stars rating={rating} interactive={true} onRatingChange={handleRatingChange} />
                </div>

                <form onSubmit={handleSubmit}>
                    <textarea
                        value={comment}
                        onChange={handleCommentChange}
                        placeholder="Leave a review... *"
                        disabled={isSubmitting}
                        maxLength={3}
                    />

                    {error && <div className={styles['error-message']}>{error}</div>}

                    <Button
                        type="submit"
                        title="Save"
                        color="white"
                        disabled={isSubmitting || isDeleting}
                        actionType="submit"
                        success={success}
                    />
                </form>
                {existingReview && (
                    <DeleteButton
                        entityName="review"
                        callbackHandler={() => setIsDeleteReviewPopupOpen(true)}
                    />
                )}
            </div>
            <Popup
                isOpen={isDeleteReviewPopupOpen}
                onClose={() => setIsDeleteReviewPopupOpen(false)}
            >
                <Deletion
                    entityName="review"
                    onProceed={handleDelete}
                    onCancel={() => setIsDeleteReviewPopupOpen(false)}
                />
            </Popup>
        </>
    );
};
