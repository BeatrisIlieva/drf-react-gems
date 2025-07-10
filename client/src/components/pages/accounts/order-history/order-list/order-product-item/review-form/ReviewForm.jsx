import { useEffect, useState } from 'react';

import { Button } from '../../../../../../reusable/button/Button';
import { Stars } from '../../../../../../reusable/stars/Stars';
import { ReviewDeleteButton } from './review-delete-button/ReviewDeleteButton';

import { useReview } from '../../../../../../../api/reviewApi';

import { useReviewFormValidation } from '../../../../../../../hooks/useReviewFormValidation';

import styles from './ReviewForm.module.scss';

export const ReviewForm = ({
    productId,
    contentType,
    onReviewSubmitted = null,
    existingReview = null,
}) => {
    const { createReview, updateReview } = useReview();
    const { error, setError, validateReview, clearRatingError, clearCommentError } =
        useReviewFormValidation();

    const [rating, setRating] = useState(existingReview?.rating || 0);
    const [comment, setComment] = useState(existingReview?.comment || '');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [success, setSuccess] = useState(false);

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

        if (!validateReview(rating, comment)) {
            return;
        }

        setIsSubmitting(true);

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
            onReviewSubmitted?.(response);

            if (!existingReview) {
                setRating(0);
                setComment('');
            }

            setTimeout(() => setSuccess(false), 3000);
        } catch {
            setError('Ensure this field has no more than 300 characters.');
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleRatingChange = newRating => {
        setRating(newRating);
        clearRatingError(newRating);
    };

    const handleCommentChange = e => {
        setComment(e.target.value);
        clearCommentError(e.target.value);
    };

    const handleReviewDeleted = () => {
        onReviewSubmitted?.(null);
        setTimeout(() => setSuccess(false), 3000);
    };

    return (
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
                    maxLength={300}
                />

                {error && <div className={styles['error-message']}>{error}</div>}

                <Button
                    type="submit"
                    title="Save"
                    color="white"
                    disabled={isSubmitting}
                    actionType="submit"
                    success={success}
                />
            </form>
            {existingReview && (
                <ReviewDeleteButton
                    existingReview={existingReview}
                    onReviewDeleted={handleReviewDeleted}
                    onError={setError}
                />
            )}
        </div>
    );
};
