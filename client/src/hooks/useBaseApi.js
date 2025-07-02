import { useCallback, useMemo } from 'react';
import { useApi } from '../hooks/useApi';
import { useAuth } from '../hooks/auth/useAuth';
import { withErrorHandling } from '../utils/apiErrorHandler';

/**
 * Base API hook that provides standardized CRUD operations
 * Follows SOLID principles and DRY methodology
 *
 * @param {string} baseUrl - The base URL for the API endpoint
 * @param {Object} options - Configuration options
 * @param {boolean} options.requireAuth - Whether authentication is required
 * @param {Function} options.transform - Optional response transformation function
 */
export const useBaseApi = (baseUrl, options = {}) => {
    const { get, post, patch, del } = useApi();
    const { isAuthenticated } = useAuth();

    const { requireAuth = false, transform = null } = options;

    const authConfig = useMemo(() => {
        return requireAuth
            ? {
                  accessRequired: isAuthenticated,
                  refreshRequired: isAuthenticated
              }
            : {};
    }, [requireAuth, isAuthenticated]);

    const apiGet = useCallback(
        async (endpoint = '', params = {}) => {
            const url = endpoint
                ? `${baseUrl}/${endpoint}`
                : `${baseUrl}/`;
            const queryString = new URLSearchParams(
                params
            ).toString();
            const fullUrl = queryString
                ? `${url}?${queryString}`
                : url;

            return withErrorHandling(
                () => get(fullUrl, authConfig),
                `GET ${fullUrl}`,
                undefined,
                transform
            );
        },
        [get, baseUrl, authConfig, transform]
    );

    const apiPost = useCallback(
        async (endpoint = '', data = null, config = {}) => {
            const url = endpoint
                ? `${baseUrl}/${endpoint}`
                : `${baseUrl}/`;

            return withErrorHandling(
                () =>
                    post(url, {
                        data,
                        ...authConfig,
                        ...config
                    }),
                `POST ${url}`,
                undefined,
                transform
            );
        },
        [post, baseUrl, authConfig, transform]
    );

    const apiPatch = useCallback(
        async (endpoint = '', data = null, config = {}) => {
            const url = endpoint
                ? `${baseUrl}/${endpoint}`
                : `${baseUrl}/`;

            return withErrorHandling(
                () =>
                    patch(url, {
                        data,
                        ...authConfig,
                        ...config
                    }),
                `PATCH ${url}`,
                undefined,
                transform
            );
        },
        [patch, baseUrl, authConfig, transform]
    );

    const apiDelete = useCallback(
        async (endpoint = '') => {
            const url = endpoint
                ? `${baseUrl}/${endpoint}`
                : `${baseUrl}/`;

            return withErrorHandling(
                () => del(url, authConfig),
                `DELETE ${url}`,
                false,
                () => true
            );
        },
        [del, baseUrl, authConfig]
    );

    return {
        get: apiGet,
        post: apiPost,
        patch: apiPatch,
        delete: apiDelete
    };
};
