import React from 'react';
import { Navigate, Outlet } from 'react-router';
import { useAuth } from '../hooks/auth/useAuth';




export const AuthGuard: React.FC = () => {
    const { isAuthenticated } = useAuth();

    if (!isAuthenticated) {
        return <Navigate to='/my-account/login' />;
    }

    return <Outlet />;
}
