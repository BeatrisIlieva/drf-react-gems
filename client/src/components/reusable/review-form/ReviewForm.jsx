import { useState, useEffect } from 'react';
import { Stars } from '../stars/Stars';
import { Button } from '../button/Button';
import { useReview } from '../../../api/reviewApi';
import { useAuth } from '../../../hooks/auth/useAuth';
import styles from './ReviewForm.module.scss';

export const ReviewForm = ({ 
    productId, 
    contentType, 
    onReviewSubmitted = null,
    existingReview = null 
}) => {
    const [rating, setRating] = useState(existingReview?.rating || 0);
    const [comment, setComment] = useState(existingReview?.comment || '');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

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

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!isAuthenticated) {
            setError('You must be logged in to submit a review');
            return;
        }

        // Clear any previous success messages when attempting to submit
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
                objectId: productId
            };

            let result;
            if (existingReview) {
                result = await updateReview(existingReview.id, reviewData);
            } else {
                result = await createReview(reviewData);
            }

            setSuccess(true);
            if (onReviewSubmitted) {
                onReviewSubmitted(result);
            }

            if (!existingReview) {
                setRating(0);
                setComment('');
            }

            setTimeout(() => setSuccess(false), 3000);
        } catch (err) {
            setError(err.message || 'Failed to submit review');
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleRatingChange = (newRating) => {
        setRating(newRating);
        // Clear validation error when user selects a rating
        if (newRating > 0 && error === 'Please select a rating') {
            setError(null);
        }
    };

    const handleCommentChange = (e) => {
        setComment(e.target.value);
        // Clear validation error when user types a comment
        if (e.target.value.trim() && error === 'Please write a comment') {
            setError(null);
        }
    };

    const handleDelete = async () => {
        if (!existingReview || !isAuthenticated) {
            return;
        }

        if (!window.confirm('Are you sure you want to delete this review?')) {
            return;
        }

        setIsDeleting(true);
        setError(null);

        try {
            await deleteReview(existingReview.id);
            setSuccess(true);
            
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

    if (!isAuthenticated) {
        return (
            <div className={styles['review-form']}>
                <p className={styles['auth-message']}>
                    Please log in to leave a review
                </p>
            </div>
        );
    }

    return (
        <div className={styles['review-form']}>
            <div className={styles['rate-header']}>
                <h5>{existingReview ? 'Update your review' : 'Rate this product'}</h5>
                <p className={styles['required-note']}>* Rating and comment are required</p>
                <Stars 
                    rating={rating}
                    interactive={true}
                    onRatingChange={handleRatingChange}
                />
            </div>

            <form onSubmit={handleSubmit}>
                <textarea
                    value={comment}
                    onChange={handleCommentChange}
                    placeholder="Leave a review... *"
                    disabled={isSubmitting}
                />
                
                {error && (
                    <div className={styles['error-message']}>
                        {error}
                    </div>
                )}
                
                {success && (
                    <div className={styles['success-message']}>
                        Review {existingReview ? (isDeleting ? 'deleted' : 'updated') : 'submitted'} successfully!
                    </div>
                )}

                <div className={styles['button-group']}>
                    <Button 
                        type="submit"
                        title={isSubmitting ? 'Submitting...' : (existingReview ? 'Update' : 'Submit')} 
                        color="white"
                        disabled={isSubmitting || isDeleting}
                        actionType="submit"
                    />
                    
                    {existingReview && (
                        <Button 
                            type="button"
                            title={isDeleting ? 'Deleting...' : 'Delete'} 
                            color="red"
                            disabled={isSubmitting || isDeleting}
                            callbackHandler={handleDelete}
                            actionType="button"
                        />
                    )}
                </div>
            </form>
        </div>
    );
};
