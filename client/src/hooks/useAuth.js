import { useContext } from 'react';
import { UserContext } from '../contexts/UserContext';

export const useAuth = () => {
    const authData = useContext(UserContext);

    return {
        ...authData,
        userId: authData._id,
        isAuthenticated: !!authData.access
    };
};
