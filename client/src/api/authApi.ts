import { useCallback } from 'react';
import { useNavigate } from 'react-router';
import { useApi } from '../hooks/useApi';
import type { UserContextPayload } from '../types/UserContext';

const baseUrl = 'http://localhost:8000/accounts';

interface UserData {
    email: string;
    password: string;
}

interface PhotoData extends FormData {
    photo?: File;
}

export const useDelete = () => {
    const { del } = useApi();

    const deleteUser = useCallback(async (): Promise<unknown> => {
        try {
            const result = await del(`${baseUrl}/delete/`, {
                accessRequired: true
            });

            return result;
        } catch (err: any) {
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
        async (userData: UserData): Promise<unknown> => {
            try {
                const result = await post(
                    `${baseUrl}/register/`,
                    {
                        data: userData
                    }
                );

                return result;
            } catch (err: any) {
                return err.data;
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
        async (
            userData: UserData
        ): Promise<UserContextPayload | undefined> => {
            try {
                const result = await post(`${baseUrl}/login/`, {
                    data: userData
                });

                return result;
            } catch (err: any) {
                console.log(err.message);
                return undefined;
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

    const logout = useCallback(async (): Promise<void> => {
        try {
            await post(`${baseUrl}/logout/`, {
                accessRequired: true,
                refreshRequired: true
            });

            navigate('/my-account/register');
        } catch (err: any) {
            console.log(err.message);
        }
    }, [post, navigate]);

    return {
        logout
    };
};

export const useDetail = () => {
    const { get } = useApi();

    const detail = useCallback(async (): Promise<unknown> => {
        try {
            const result = await get(`${baseUrl}/detail/`, {
                accessRequired: true
            });

            return result;
        } catch (err: any) {
            console.log(err.message);
        }
    }, [get]);

    return {
        detail
    };
};

export const useUploadPhoto = () => {
    const { patch } = useApi();

    const upload = useCallback(
        async (data: PhotoData): Promise<unknown> => {
            try {
                const result = await patch(`${baseUrl}/photo/`, {
                    data,
                    accessRequired: true,
                    refreshRequired: true,
                    contentType: 'multipart/form-data'
                });

                return result;
            } catch (err: any) {
                console.log(err.message);
            }
        },
        [patch]
    );

    return {
        upload
    };
};

export const useGetPhoto = () => {
    const { get } = useApi();

    const getPhoto = useCallback(async (): Promise<unknown> => {
        try {
            const result = await get(`${baseUrl}/photo/`, {
                accessRequired: true,
                refreshRequired: true
            });

            return result;
        } catch (err: any) {
            console.log(err.message);
        }
    }, [get]);

    return {
        getPhoto
    };
};
