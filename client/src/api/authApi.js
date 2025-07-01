import { useCallback } from 'react';
import { useNavigate } from 'react-router';
import { useApi } from '../hooks/useApi';
import { HOST } from '../constants/host';

const baseUrl = `${HOST}/accounts`;

export const useDelete = () => {
    const { del } = useApi();

    const deleteUser = useCallback(async () => {
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

export const useRegister = () => {
    const { post } = useApi();

    const register = useCallback(
        async (userData) => {
            try {
                const result = await post(
                    `${baseUrl}/register/`,
                    {
                        data: userData
                    }
                );

                return result;
            } catch (err) {
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
        async (userData) => {
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

    const logout = useCallback(async () => {
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

export const useDetail = () => {
    const { get } = useApi();

    const detail = useCallback(async () => {
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

export const useUploadPhoto = () => {
    const { patch } = useApi();

    const upload = useCallback(
        async (data) => {
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

export const useGetPhoto = () => {
    const { get } = useApi();

    const getPhoto = useCallback(async () => {
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

export const useGetPersonalInfo = () => {
    const { get } = useApi();

    const getPersonalInfo = useCallback(async () => {
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
        async (personalData) => {
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
            } catch (err) {
                return err.data;
            }
        },
        [patch]
    );

    return {
        updatePersonalInfo
    };
};

export const useChangePassword = () => {
    const { patch } = useApi();

    const changePassword = useCallback(
        async (passwordData) => {
            try {
                const result = await patch(
                    `${baseUrl}/change-password/`,
                    {
                        data: passwordData,
                        accessRequired: true,
                        refreshRequired: true
                    }
                );

                return (
                    result || {
                        message: 'Password changed successfully'
                    }
                );
            } catch (err) {
                return {
                    error:
                        err.message ||
                        'Failed to change password',
                    ...err.data
                };
            }
        },
        [patch]
    );

    return {
        changePassword
    };
};
