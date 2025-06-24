import { useContext } from 'react';
import { UserContext } from '../../contexts/UserContext';
import type { UserContextType } from '../../types/User';

interface AuthData extends UserContextType {
    userId: string | undefined;
    isAuthenticated: boolean;
}

export const useAuth = (): AuthData => {
    const authData = useContext(UserContext);

    return {
        ...authData,
        userId: authData._id,
        isAuthenticated: !!authData.access
    };
}
