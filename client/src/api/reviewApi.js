import { useCallback } from 'react';

import { useApi } from '../hooks/useApi';

import { keysToCamelCase } from '../utils/convertToCamelCase';
import { keysToSnakeCase } from '../utils/convertToSnakeCase';

import { HOST } from '../constants/host';

const baseUrl = `${HOST}/api/products/reviews`;

export const useReview = () => {
    const { get, post, put, del } = useApi();

    const createReview = useCallback(
        async reviewData => {
            try {
                const data = keysToSnakeCase(reviewData);
                const response = await post(`${baseUrl}/`, {
                    data,
                    accessRequired: true,
                    refreshRequired: true,
                });
                return keysToCamelCase(response);
            } catch (error) {
                console.error('Create review error:', error);
                throw error;
            }
        },
        [post]
    );

    const updateReview = useCallback(
        async (reviewId, reviewData) => {
            try {
                const data = keysToSnakeCase(reviewData);
                const response = await put(`${baseUrl}/${reviewId}/`, {
                    data,
                    accessRequired: true,
                    refreshRequired: true,
                });
                return keysToCamelCase(response);
            } catch (error) {
                console.error('Update review error:', error);
                throw error;
            }
        },
        [put]
    );

    const deleteReview = useCallback(
        async reviewId => {
            try {
                await del(`${baseUrl}/${reviewId}/`, {
                    accessRequired: true,
                    refreshRequired: true,
                });
                return true;
            } catch (error) {
                console.error('Delete review error:', error);
                throw error;
            }
        },
        [del]
    );

    const getUserReview = useCallback(
        async (contentType, objectId) => {
            try {
                const response = await get(`${baseUrl}/user-review/${contentType}/${objectId}/`, {
                    accessRequired: true,
                    refreshRequired: true,
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
        [get]
    );

    const approveReview = useCallback(
        async reviewId => {
            try {
                const response = await post(`${baseUrl}/${reviewId}/approve/`, {
                    accessRequired: true,
                    refreshRequired: true,
                });
                return keysToCamelCase(response);
            } catch (error) {
                console.error('Approve review error:', error);
                throw error;
            }
        },
        [post]
    );

    const unapproveReview = useCallback(
        async reviewId => {
            try {
                const response = await post(`${baseUrl}/${reviewId}/unapprove/`, {
                    accessRequired: true,
                    refreshRequired: true,
                });
                return keysToCamelCase(response);
            } catch (error) {
                console.error('Unapprove review error:', error);
                throw error;
            }
        },
        [post]
    );

    return {
        createReview,
        updateReview,
        deleteReview,
        getUserReview,
        approveReview,
        unapproveReview,
    };
};

export const useReviewApi = () => {
    const { approveReview, unapproveReview } = useReview();

    return {
        approveReview,
        unapproveReview,
    };
};
