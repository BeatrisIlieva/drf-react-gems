import { useContext, useCallback, useMemo } from 'react';
import { UserContext } from '../contexts/UserContext';
import { useAuthRefresh } from './useAuthRefresh';
import { useGuest } from './useGuest';

export const useApi = () => {
    const { access, refresh } = useContext(UserContext);
    const { authRefresh } = useAuthRefresh();
    const { guestId } = useGuest();

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
                        bodyData.append('refresh', refresh);
                    }

                    options.body = bodyData;

                    delete options.headers['Content-Type'];
                } else {
                    if (refreshRequired) {
                        bodyData = { ...bodyData, refresh };
                    }

                    options.body = JSON.stringify(bodyData);

                    if (guestId) {
                        options.headers['Guest-Id'] = guestId;
                    }
                }
            }

            const response = await fetch(url, options);

            const json = await response.json();

            if (!response.ok) {
                if (response.status === 401) {
                    if (json.error === 'Invalid username or password') {
                        return 'Invalid username or password';
                    }

                    await authRefresh();
                }

                const error = new Error('Request failed');
                error.status = response.status;
                error.data = json;
                throw error;
            }

            return json;
        },
        [access, refresh, authRefresh, guestId]
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
