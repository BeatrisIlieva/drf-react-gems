import { useContext } from 'react';
import { UserContext } from '../../contexts/UserContext';
import type { UserContextType } from '../../types/UserContext';

interface UseAuthResult extends UserContextType {
    userId: string;
    isAuthenticated: boolean;
}

export const useAuth = (): UseAuthResult => {
    const authData = useContext<UserContextType>(UserContext);

    return {
        ...authData,
        userId: authData._id,
        isAuthenticated: Boolean(authData.access)
    };
};
