import { Navigate, Outlet } from "react-router";
import { useAuth } from "../hooks/useAuth";

export const AuthGuard = () => {
    const { isAuthenticated } = useAuth();

    if (!isAuthenticated) {
        return <Navigate to="/my-account/login" />;
    }

    return <Outlet />;
};
