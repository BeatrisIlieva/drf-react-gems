import { useCallback } from 'react';
import { useNavigate } from 'react-router';
import { useApi } from '../hooks/useApi';
import { HOST } from '../constants/host';

const baseUrl = `${HOST}/accounts`;

interface DeleteResponse {
    success: boolean;
    message?: string;
}

export const useDelete = () => {
    const { del } = useApi();

    const deleteUser = useCallback(async (): Promise<
        DeleteResponse | undefined
    > => {
        try {
            const result = await del(`${baseUrl}/delete/`, {
                accessRequired: true
            });

            return result;
        } catch (err) {
            console.log(
                err instanceof Error ? err.message : String(err)
            );
            return undefined;
        }
    }, [del]);

    return {
        deleteUser
    };
};

interface RegisterRequest {
    email: string;
    username: string;
    password: string;
}

interface LoginRequest {
    email_or_username: string;
    password: string;
}

interface RegisterResponse {
    id?: string;
    email?: string;
    username?: string;
    access?: string;
    refresh?: string;
    [key: string]: string | undefined;
}

export const useRegister = () => {
    const { post } = useApi();

    const register = useCallback(
        async (
            userData: RegisterRequest
        ): Promise<RegisterResponse> => {
            try {
                const result = await post(
                    `${baseUrl}/register/`,
                    {
                        data: userData
                    }
                );

                return result;
            } catch (err: unknown) {
                return (err as { data: RegisterResponse }).data;
            }
        },
        [post]
    );

    return {
        register
    };
};

interface LoginResponse {
    id?: string;
    email?: string;
    username?: string;
    access?: string;
    refresh?: string;
}

export const useLogin = () => {
    const { post } = useApi();

    const login = useCallback(
        async (
            userData: LoginRequest
        ): Promise<LoginResponse | undefined> => {
            try {
                const result = await post(`${baseUrl}/login/`, {
                    data: userData
                });

                return result;
            } catch (err) {
                console.log(
                    err instanceof Error
                        ? err.message
                        : String(err)
                );
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
        } catch (err) {
            console.log(
                err instanceof Error ? err.message : String(err)
            );
        }
    }, [post, navigate]);

    return {
        logout
    };
};

interface UserDetailResponse {
    id?: string;
    email?: string;
    first_name?: string;
    last_name?: string;
    [key: string]: any;
}

export const useDetail = () => {
    const { get } = useApi();

    const detail = useCallback(async (): Promise<
        UserDetailResponse | undefined
    > => {
        try {
            const result = await get(`${baseUrl}/detail/`, {
                accessRequired: true
            });

            return result;
        } catch (err) {
            console.log(
                err instanceof Error ? err.message : String(err)
            );
            return undefined;
        }
    }, [get]);

    return {
        detail
    };
};

interface PhotoUploadResponse {
    success: boolean;
    url?: string;
    message?: string;
}

export const useUploadPhoto = () => {
    const { patch } = useApi();

    const upload = useCallback(
        async (
            data: FormData
        ): Promise<PhotoUploadResponse | undefined> => {
            try {
                const result = await patch(`${baseUrl}/photo/`, {
                    data,
                    accessRequired: true,
                    refreshRequired: true,
                    contentType: 'multipart/form-data'
                });

                return result;
            } catch (err) {
                console.log(
                    err instanceof Error
                        ? err.message
                        : String(err)
                );
                return undefined;
            }
        },
        [patch]
    );

    return {
        upload
    };
};

interface PhotoResponse {
    url?: string;
    [key: string]: any;
}

export const useGetPhoto = () => {
    const { get } = useApi();

    const getPhoto = useCallback(async (): Promise<
        PhotoResponse | undefined
    > => {
        try {
            const result = await get(`${baseUrl}/photo/`, {
                accessRequired: true,
                refreshRequired: true
            });

            return result;
        } catch (err) {
            console.log(
                err instanceof Error ? err.message : String(err)
            );
            return undefined;
        }
    }, [get]);

    return {
        getPhoto
    };
};

interface PersonalInfoResponse {
    firstName?: string;
    lastName?: string;
    phoneNumber?: string;
    [key: string]: any;
}

export const useGetPersonalInfo = () => {
    const { get } = useApi();

    const getPersonalInfo = useCallback(async (): Promise<
        PersonalInfoResponse | undefined
    > => {
        try {
            const result = await get(`${baseUrl}/profile/`, {
                accessRequired: true,
                refreshRequired: true
            });

            return result;
        } catch (err) {
            console.log(
                err instanceof Error ? err.message : String(err)
            );
            return undefined;
        }
    }, [get]);

    return {
        getPersonalInfo
    };
};

export const useUpdatePersonalInfo = () => {
    const { patch } = useApi();

    const updatePersonalInfo = useCallback(
        async (
            personalData: Record<string, any>
        ): Promise<PersonalInfoResponse | undefined> => {
            try {
                const result = await patch(
                    `${baseUrl}/profile/`,
                    {
                        data: personalData,
                        accessRequired: true,
                        refreshRequired: true
                    }
                );

                return result;
            } catch (err: any) {
                return err.data;
            }
        },
        [patch]
    );

    return {
        updatePersonalInfo
    };
};
