import { useCallback, useEffect, useState } from 'react';

import { useNavigate } from 'react-router';

import { ReviewForm } from './review-form/ReviewForm';

import { useReview } from '../../../../../../api/reviewApi';

import { useAuth } from '../../../../../../hooks/useAuth';

import styles from './OrderProductItem.module.scss';

export const OrderProductItem = ({ product }) => {
    const { getUserReview } = useReview();
    const { isAuthenticated } = useAuth();
    const navigate = useNavigate();

    const [existingReview, setExistingReview] = useState(null);
    const [isLoadingReview, setIsLoadingReview] = useState(false);

    const productInfo = product.productInfo;
    const contentType = product.productContentType;
    const objectId = product.productObjectId;

    useEffect(() => {
        const loadReview = async () => {
            if (isAuthenticated && contentType && objectId) {
                setIsLoadingReview(true);
                try {
                    const review = await getUserReview(contentType, objectId);
                    setExistingReview(review);
                } catch (error) {
                    console.error('Error loading review:', error);
                } finally {
                    setIsLoadingReview(false);
                }
            } else {
                setExistingReview(null);
                setIsLoadingReview(false);
            }
        };

        if (contentType && objectId) {
            loadReview();
        }
    }, [isAuthenticated, contentType, objectId]);

    const handleReviewSubmitted = newReview => {
        setExistingReview(newReview);
    };

    const navigateToProductItem = useCallback(() => {
        navigate(`/products/${productInfo.category.toLowerCase() + 's'}/${productInfo.productId}`);
    }, [navigate, productInfo.category, productInfo.productId]);

    return (
        <div className={styles['order-product-item']}>
            {existingReview && (
                <p className={existingReview.approved ? styles['approved'] : styles['unapproved']}>{existingReview.approved ? 'approved' : 'waiting for approval'}</p>
            )}
            <div className={styles['product-details']}>
                <div className={styles['thumbnail']} onClick={navigateToProductItem}>
                    <img
                        src={productInfo.firstImage}
                        alt={`${productInfo.collection} ${productInfo.category}`}
                    />
                </div>

                <div className={styles['product-info']}>
                    <h4>{`${productInfo.collection} ${productInfo.category}`}</h4>
                    <p>{`${productInfo.color} ${productInfo.stone} set in ${productInfo.metal}`}</p>
                </div>
            </div>

            <div className={styles['review-section']}>
                {isAuthenticated && contentType && objectId ? (
                    isLoadingReview ? (
                        <p>Loading review...</p>
                    ) : (
                        <ReviewForm
                            productId={objectId}
                            contentType={contentType}
                            existingReview={existingReview}
                            onReviewSubmitted={handleReviewSubmitted}
                        />
                    )
                ) : !isAuthenticated ? (
                    <p>Please log in to leave a review</p>
                ) : (
                    <p>Product information incomplete - cannot load reviews</p>
                )}
            </div>
        </div>
    );
};
