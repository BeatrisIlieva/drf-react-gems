import { useState } from 'react';

export const useReviewFormValidation = () => {
    const [error, setError] = useState(null);

    const validateReview = (rating, comment) => {
        if (rating === 0) {
            setError('Please select a rating');
            return false;
        }

        if (!comment.trim()) {
            setError('Please write a comment');
            return false;
        }

        setError(null);
        return true;
    };

    const clearRatingError = rating => {
        if (rating > 0 && error === 'Please select a rating') {
            setError(null);
        }
    };

    const clearCommentError = comment => {
        if (comment.trim() && error === 'Please write a comment') {
            setError(null);
        }
    };

    const clearError = () => setError(null);

    return {
        error,
        setError,
        validateReview,
        clearRatingError,
        clearCommentError,
        clearError,
    };
};
