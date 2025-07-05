import { useContext, useCallback, useMemo } from 'react';

import { useAuthRefresh } from './auth/useAuthRefresh';
import { useGuest } from './useGuest';

import { UserContext } from '../contexts/UserContext';

export const useApi = () => {
    const { access, refresh } = useContext(UserContext);
    const { authRefresh } = useAuthRefresh();
    const { getGuestData } = useGuest();

    const request = useCallback(
        async (
            method,
            url,
            {
                data = null,
                accessRequired = false,
                refreshRequired = false,
                contentType = 'application/json'
            } = {}
        ) => {
            const options = {
                method,
                headers: {
                    'Content-Type': contentType
                }
            };

            // Get guest ID dynamically to ensure we have the latest value
            const currentGuestId = getGuestData();
            if (currentGuestId) {
                options.headers['Guest-Id'] = currentGuestId;
            }

            if (accessRequired) {
                options.headers.Authorization = `Bearer ${access}`;
            }

            if (method !== 'GET') {
                let bodyData = data;

                if (contentType === 'multipart/form-data') {
                    if (!(bodyData instanceof FormData)) {
                        throw new Error(
                            'Data must be a FormData instance for multipart/form-data'
                        );
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

            // Check if response has content before trying to parse JSON
            let json = null;
            const responseContentType =
                response.headers.get('content-type');
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
                        console.warn(
                            'Failed to parse JSON response:',
                            responseText
                        );
                        json = null;
                    }
                }
            }

            if (!response.ok) {
                // For 401 errors, check if we have a JSON response with error details
                if (response.status === 401 && json) {
                    if (
                        json?.error ===
                        'Invalid username or password'
                    ) {
                        return 'Invalid username or password';
                    }
                    await authRefresh();
                }

                // Create error with additional context
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
        // eslint-disable-next-line react-hooks/exhaustive-deps
        [access, refresh, authRefresh]
    );

    return useMemo(
        () => ({
            get: request.bind(null, 'GET'),
            post: request.bind(null, 'POST'),
            put: request.bind(null, 'PUT'),
            patch: request.bind(null, 'PATCH'),
            del: request.bind(null, 'DELETE')
        }),
        [request]
    );
};
