import { Navigate, Outlet } from 'react-router';

import { useAuth } from '../hooks/useAuth';

export const AdminGuard = () => {
    const { permissions, isAuthenticated } = useAuth();
    const isReviewer = permissions?.includes('products.approve_review');

    if (!isReviewer) {
        if (isAuthenticated) {
            return <Navigate to="/my-account/details" />;
        }

        return <Navigate to="/my-account/login" />;
    }

    return <Outlet />;
};
