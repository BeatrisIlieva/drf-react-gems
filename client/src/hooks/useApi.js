import { useCallback, useMemo } from 'react';

import { useNavigate } from 'react-router';

import { useAuthRefresh } from './useAuthRefresh';

import { useUserContext } from '../contexts/UserContext';

export const useApi = () => {
    const { access, refresh } = useUserContext();
    const { authRefresh } = useAuthRefresh();
    const navigate = useNavigate();

    const request = useCallback(
        async (
            method,
            url,
            {
                data = null,
                accessRequired = false,
                refreshRequired = false,
                contentType = 'application/json',
            } = {}
        ) => {
            const options = {
                method,
                headers: {
                    'Content-Type': contentType,
                },
            };

            if (accessRequired) {
                options.headers.Authorization = `Bearer ${access}`;
            }

            if (method !== 'GET') {
                let bodyData = data;

                if (contentType === 'multipart/form-data') {
                    if (!(bodyData instanceof FormData)) {
                        throw new Error('Data must be a FormData instance for multipart/form-data');
                    }

                    if (refreshRequired) {
                        if (refresh) {
                            bodyData.append('refresh', refresh);
                        }
                    }

                    options.body = bodyData;

                    delete options.headers['Content-Type'];
                } else {
                    if (refreshRequired && refresh) {
                        bodyData = { ...bodyData, refresh };
                    }

                    options.body = JSON.stringify(bodyData);
                }
            }

            const response = await fetch(url, options);

            let json = null;
            const responseContentType = response.headers.get('content-type');
            const hasContent =
                response.status !== 204 &&
                response.status !== 205 &&
                responseContentType &&
                responseContentType.includes('application/json');

            if (hasContent) {
                const responseText = await response.text();
                if (responseText && responseText.trim()) {
                    try {
                        json = JSON.parse(responseText);
                    } catch {
                        console.warn('Failed to parse JSON response:', responseText);
                        json = null;
                    }
                }
            }

            if (!response.ok) {
                if (response.status === 401) {
                    if (json?.error === 'Invalid username or password') {
                        return 'Invalid username or password';
                    }

                    try {
                        await authRefresh();

                        // Get fresh token from localStorage
                        const authDataString = localStorage.getItem('auth');
                        let freshToken = null;

                        if (authDataString) {
                            try {
                                const authData = JSON.parse(authDataString);
                                freshToken = authData.access;
                            } catch (e) {
                                console.error('Failed to parse auth data:', e);
                            }
                        }

                        // Reconstruct the retry request properly
                        const retryOptions = {
                            method: options.method,
                            headers: {},
                            body: options.body,
                        };

                        // Add authorization header with fresh token
                        if (freshToken) {
                            retryOptions.headers.Authorization = `Bearer ${freshToken}`;
                        }

                        // Only set Content-Type if it's NOT multipart/form-data
                        // For FormData, the browser will set the correct Content-Type with boundary
                        if (contentType !== 'multipart/form-data') {
                            retryOptions.headers['Content-Type'] = contentType;
                        }

                        const retryResponse = await fetch(url, retryOptions);

                        let retryJson = null;
                        const retryContentType = retryResponse.headers.get('content-type');
                        const retryHasContent =
                            retryResponse.status !== 204 &&
                            retryResponse.status !== 205 &&
                            retryContentType &&
                            retryContentType.includes('application/json');

                        if (retryHasContent) {
                            const retryResponseText = await retryResponse.text();
                            if (retryResponseText && retryResponseText.trim()) {
                                try {
                                    retryJson = JSON.parse(retryResponseText);
                                } catch {
                                    console.warn(
                                        'Failed to parse retry JSON response:',
                                        retryResponseText
                                    );
                                    retryJson = null;
                                }
                            }
                        }

                        if (!retryResponse.ok) {
                            console.error('Retry failed with status:', retryResponse.status);
                            const retryError = new Error(
                                retryJson?.message ||
                                    retryJson?.error ||
                                    `HTTP ${retryResponse.status}: ${retryResponse.statusText}`
                            );
                            retryError.status = retryResponse.status;
                            retryError.data = retryJson;
                            retryError.url = url;
                            throw retryError;
                        }

                        return retryJson;
                    } catch (refreshError) {
                        console.error('Token refresh failed:', refreshError);
                        throw refreshError;
                    }
                }

                if (response.status === 404) {
                    navigate('/page-not-found', { replace: true });
                    return;
                }

                const error = new Error(
                    json?.message ||
                        json?.error ||
                        `HTTP ${response.status}: ${response.statusText}`
                );
                error.status = response.status;
                error.data = json;
                error.url = url;
                throw error;
            }

            return json;
        },
        [access, refresh, authRefresh, navigate]
    );

    return useMemo(
        () => ({
            get: request.bind(null, 'GET'),
            post: request.bind(null, 'POST'),
            put: request.bind(null, 'PUT'),
            patch: request.bind(null, 'PATCH'),
            del: request.bind(null, 'DELETE'),
        }),
        [request]
    );
};
