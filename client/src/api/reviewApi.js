import { useCallback } from 'react';

import { useApi } from '../hooks/useApi';
import { useAuth } from '../hooks/useAuth';

import { keysToCamelCase } from '../utils/convertToCamelCase';
import { keysToSnakeCase } from '../utils/convertToSnakeCase';

import { HOST } from '../constants/host';

const baseUrl = `${HOST}/api/products/reviews`;

export const useReview = () => {
    const { get, post, put, del } = useApi();
    const { isAuthenticated } = useAuth();

    const createReview = useCallback(
        async reviewData => {
            try {
                const data = keysToSnakeCase(reviewData);
                const response = await post(`${baseUrl}/`, {
                    data,
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated,
                });
                return keysToCamelCase(response);
            } catch (error) {
                console.error('Create review error:', error);
                throw error;
            }
        },
        [post, isAuthenticated]
    );

    const updateReview = useCallback(
        async (reviewId, reviewData) => {
            try {
                const data = keysToSnakeCase(reviewData);
                const response = await put(`${baseUrl}/${reviewId}/`, {
                    data,
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated,
                });
                return keysToCamelCase(response);
            } catch (error) {
                console.error('Update review error:', error);
                throw error;
            }
        },
        [put, isAuthenticated]
    );

    const deleteReview = useCallback(
        async reviewId => {
            try {
                await del(`${baseUrl}/${reviewId}/`, {
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated,
                });
                return true;
            } catch (error) {
                console.error('Delete review error:', error);
                throw error;
            }
        },
        [del, isAuthenticated]
    );

    const getUserReview = useCallback(
        async (contentType, objectId) => {
            if (!isAuthenticated) {
                return null;
            }

            try {
                const response = await get(`${baseUrl}/user-review/${contentType}/${objectId}/`, {
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated,
                });
                return keysToCamelCase(response);
            } catch (error) {
                if (error.status === 404) {
                    return null;
                }
                if (error.status === 401) {
                    return null;
                }
                console.error('Get user review error:', error);
                throw error;
            }
        },
        [get, isAuthenticated]
    );

    const getApprovedReviews = useCallback(
        async (contentType, objectId) => {
            try {
                const response = await get(
                    `${baseUrl}/?content_type=${contentType}&object_id=${objectId}`,
                    {
                        accessRequired: false,
                        refreshRequired: false,
                    }
                );
                return keysToCamelCase(response);
            } catch (error) {
                if (error.status === 404) {
                    return [];
                }
                throw error;
            }
        },
        [get]
    );

    const approveReview = useCallback(
        async reviewId => {
            try {
                const response = await post(`${baseUrl}/${reviewId}/approve/`, {
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated,
                });
                return keysToCamelCase(response);
            } catch (error) {
                console.error('Approve review error:', error);
                throw error;
            }
        },
        [post, isAuthenticated]
    );

    const unapproveReview = useCallback(
        async reviewId => {
            try {
                const response = await post(`${baseUrl}/${reviewId}/unapprove/`, {
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated,
                });
                return keysToCamelCase(response);
            } catch (error) {
                console.error('Unapprove review error:', error);
                throw error;
            }
        },
        [post, isAuthenticated]
    );

    const getPendingReviews = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}/pending/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated,
            });
            return keysToCamelCase(response);
        } catch (error) {
            console.error('Get pending reviews error:', error);
            throw error;
        }
    }, [get, isAuthenticated]);

    const getAllReviews = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated,
            });
            return keysToCamelCase(response);
        } catch (error) {
            console.error('Get all reviews error:', error);
            throw error;
        }
    }, [get, isAuthenticated]);

    return {
        createReview,
        updateReview,
        deleteReview,
        getUserReview,
        getApprovedReviews,

        approveReview,
        unapproveReview,
        getPendingReviews,
        getAllReviews,
    };
};

export const useReviewApi = () => {
    const { approveReview, unapproveReview } = useReview();

    return {
        approveReview,
        unapproveReview,
    };
};
