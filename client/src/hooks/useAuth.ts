import { useContext } from 'react';
import { UserContext } from '../contexts/UserContext';
import type { UserContextType } from '../types/UserContext';

interface UseAuthReturn extends UserContextType {
    userId: string;
    isAuthenticated: boolean;
}

export const useAuth = (): UseAuthReturn => {
    const authData = useContext<UserContextType>(UserContext);

    return {
        ...authData,
        userId: authData._id,
        isAuthenticated: Boolean(authData.access)
    };
};
