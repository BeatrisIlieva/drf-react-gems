import { useCallback } from 'react';

import { useUserContext } from '../contexts/UserContext';

let isRefreshing = false;
let refreshPromise = null;

export const useAuthRefresh = () => {
    const { userLogoutHandler, setAuthData } = useUserContext();

    const authRefresh = useCallback(async () => {
        if (isRefreshing) {
            return refreshPromise;
        }

        const authDataString = localStorage.getItem('auth');

        if (!authDataString) {
            userLogoutHandler();
            return;
        }

        let authData;
        try {
            authData = JSON.parse(authDataString);
        } catch {
            userLogoutHandler();
            return;
        }

        const refresh = authData.refresh;
        if (!refresh) {
            userLogoutHandler();
            return;
        }

        isRefreshing = true;
        refreshPromise = (async () => {
            try {
                const response = await fetch('http://localhost:8000/api/accounts/token/refresh/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ refresh }),
                });

                if (!response.ok) {
                    if (response.status === 401) {
                        userLogoutHandler();
                    }
                    const errorText = await response.text();
                    throw new Error(`Failed to refresh token: ${response.status} - ${errorText}`);
                }

                const data = await response.json();

                if (data.access) {
                    const newAuthData = {
                        ...authData,
                        access: data.access,
                    };

                    localStorage.setItem('auth', JSON.stringify(newAuthData));
                    setAuthData(newAuthData);
                } else {
                    throw new Error('No access token in response');
                }
            } catch (err) {
                console.error('Refresh error:', err instanceof Error ? err.message : String(err));
                userLogoutHandler();
                throw err;
            } finally {
                isRefreshing = false;
                refreshPromise = null;
            }
        })();

        return refreshPromise;
    }, [userLogoutHandler, setAuthData]);

    return {
        authRefresh,
    };
};
