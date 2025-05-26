import { useContext, useCallback, useMemo } from 'react';
import { UserContext } from '../contexts/UserContext';
import { useAuthRefresh } from './useAuthRefresh';

export const useApi = () => {
    const { access, refresh } = useContext(UserContext);
    const { authRefresh } = useAuthRefresh();

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

            // if (method !== 'GET') {
            //     let bodyData = data ? { ...data } : {};

            //     if (refreshRequired) {
            //         bodyData.refresh = refresh;
            //     }

            //     if (contentType === 'multipart/form-data') {
            //         options.body = bodyData;
            //         delete options.headers['Content-Type'];
            //     } else {
            //         options.body = JSON.stringify(bodyData);
            //     }

            // }

            if (method !== 'GET') {
                let bodyData = data;
            
                if (contentType === 'multipart/form-data') {
                    // Make sure it's a FormData instance
                    if (!(bodyData instanceof FormData)) {
                        throw new Error('Data must be a FormData instance for multipart/form-data');
                    }
            
                    if (refreshRequired) {
                        bodyData.append('refresh', refresh);
                    }
            
                    options.body = bodyData;
            
                    // Remove Content-Type so the browser sets it (with boundary)
                    delete options.headers['Content-Type'];
                } else {
                    if (refreshRequired) {
                        bodyData = { ...bodyData, refresh };
                    }
            
                    options.body = JSON.stringify(bodyData);
                }
            }

            const response = await fetch(url, options);

            const json = await response.json();

            if (!response.ok) {
                if (response.status === 401) {
                    if (json.error === 'Invalid username or password') {
                        return 'Invalid username or password';
                    }

                    return authRefresh();
                }

                const error = new Error('Request failed');
                error.status = response.status;
                error.data = json;
                // throw error;
            }

            return json;
        },
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
