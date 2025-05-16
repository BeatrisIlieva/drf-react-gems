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
                refreshRequired = false
            } = {}
        ) => {
            const options = {
                method,
                headers: {
                    'Content-Type': 'application/json'
                }
            };

            if (accessRequired) {
                options.headers.Authorization = `Bearer ${access}`;
            }

            if (method !== 'GET') {
                let bodyData = data ? { ...data } : {};

                if (refreshRequired) {
                    bodyData.refresh = refresh;
                }

                options.body = JSON.stringify(bodyData);
            }

            const response = await fetch(url, options);

            const json = await response.json();

            if (!response.ok) {
                if (response.status === 401) {
                    return authRefresh();
                }

                const error = new Error('Request failed');
                error.status = response.status;
                error.data = json;
                throw error;
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
