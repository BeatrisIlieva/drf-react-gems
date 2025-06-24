import useUserContext from '../../contexts/UserContext';
import { useCallback } from 'react';
import type { UserData } from '../../types/User';

interface AuthRefreshReturn {
    authRefresh: () => Promise<void>;
}

export const useAuthRefresh = (): AuthRefreshReturn => {
    const { userLogoutHandler } = useUserContext();

    const authRefresh = useCallback(async () => {
        const authDataString = localStorage.getItem('auth');

        if (!authDataString) {
            userLogoutHandler();
            return;
        }

        let authData: UserData;
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

        try {
            const response = await fetch('http://localhost:8000/accounts/token/refresh/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh })
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
                localStorage.setItem(
                    'auth',
                    JSON.stringify({
                        ...authData,
                        access: data.access
                    })
                );
                console.log('Access token refreshed');
            } else {
                throw new Error('No access token in response');
            }
        } catch (err) {
            console.error('Refresh error:', err instanceof Error ? err.message : String(err));
            userLogoutHandler();
        }
    }, [userLogoutHandler]);

    return {
        authRefresh
    };
};
