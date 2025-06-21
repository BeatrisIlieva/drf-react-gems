import { useContext, useCallback, useMemo } from 'react';
import { UserContext} from '../contexts/UserContext';
import { useAuthRefresh } from './auth/useAuthRefresh';
import { useGuest } from './useGuest';
import type { UserContextType } from '../types/UserContext';

interface RequestOptions {
    data?: any;
    accessRequired?: boolean;
    refreshRequired?: boolean;
    contentType?: string;
}

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

interface ApiError extends Error {
    status?: number;
    data?: unknown;
}

export const useApi = () => {
    const { access, refresh } = useContext<UserContextType>(UserContext);
    const { authRefresh } = useAuthRefresh();
    const { getGuestData } = useGuest();

    const guestId = useMemo(() => getGuestData(), [getGuestData]);

    const request = useCallback(
        async (
            method: HttpMethod,
            url: string,
            {
                data = null,
                accessRequired = false,
                refreshRequired = false,
                contentType = 'application/json'
            }: RequestOptions = {}
        ): Promise<any> => {
            const options: RequestInit & { headers: Record<string, string> } = {
                method,
                headers: {
                    'Content-Type': contentType
                }
            };

            if (guestId) {
                options.headers['Guest-Id'] = guestId;
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
                        bodyData.append('refresh', refresh);
                    }

                    options.body = bodyData;

                    delete options.headers['Content-Type'];
                } else {
                    if (refreshRequired) {
                        bodyData = { ...bodyData, refresh };
                    }

                    options.body = JSON.stringify(bodyData);
                }
            }

            const response = await fetch(url, options);
            let json;
            try {
                json = await response.json();
            } catch {
                json = null;
            }

            if (!response.ok) {
                if (response.status === 401) {
                    if (json?.error === 'Invalid username or password') {
                        return 'Invalid username or password';
                    }

                    await authRefresh();
                }

                const error: ApiError = new Error('Request failed');
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
