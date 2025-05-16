import { useCallback } from 'react';
import { useNavigate } from 'react-router';
import { useApi } from '../hooks/useApi';

const baseUrl = 'http://localhost:8000/accounts';

export const useDelete = () => {
    const { del } = useApi();

    const deleteUser = useCallback(async () => {
        try {
            const result = await del(`${baseUrl}/delete/`, {
                accessRequired: true
            });

            return result;
        } catch (err) {
            console.log(err.message);
        }
    }, [del]);

    return {
        deleteUser
    };
};

export const useRegister = () => {
    const { post } = useApi();

    const register = useCallback(
        async (userData) => {
            try {
                const result = await post(`${baseUrl}/register/`, {
                    data: userData
                });

                console.log(result)

                return result;
            } catch (err) {
                return err.data
            }
        },
        [post]
    );

    return {
        register
    };
};

export const useLogin = () => {
    const { post } = useApi();

    const login = useCallback(
        async (userData) => {
            try {
                const result = post(`${baseUrl}/login/`, { data: userData });

                return result;
            } catch (err) {
                console.log(err.message);
            }
        },
        [post]
    );

    return {
        login
    };
};

export const useLogout = () => {
    const { post } = useApi();

    const navigate = useNavigate();

    const logout = useCallback(async () => {
        try {
            await post(`${baseUrl}/logout/`, {
                accessRequired: true,
                refreshRequired: true
            });

            navigate('/my-account/register');
        } catch (err) {
            console.log(err.message);
        }
    }, [post, navigate]);

    return {
        logout
    };
};

export const useDetail = () => {
    const { get } = useApi();

    const detail = useCallback(async () => {
        try {
            const result = await get(`${baseUrl}/detail/`, {
                accessRequired: true
            });

            return result;
        } catch (err) {
            console.log(err.message);
        }
    }, [get]);

    return {
        detail
    };
};
