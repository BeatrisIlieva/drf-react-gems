import { useCallback } from 'react';
import { useNavigate } from 'react-router';
import { useApi } from '../../hooks/useApi';
import { useAuth } from '../../hooks/auth/useAuth';
import { usePhoto } from './usePhotoApi';
import { useProfile } from './useProfileApi';
import { HOST } from '../../constants/host';

const baseUrl = `${HOST}/api/accounts`;

export const useAuthentication = () => {
    const { post, del } = useApi();
    const { isAuthenticated } = useAuth();
    const navigate = useNavigate();

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
            } catch (error) {
                console.error(
                    'Error during registration:',
                    error
                );
                return error.data;
            }
        },
        [post]
    );

    const login = useCallback(
        async (userData) => {
            try {
                const result = await post(`${baseUrl}/login/`, {
                    data: userData
                });
                return result;
            } catch (error) {
                console.error('Error during login:', error);
                return undefined;
            }
        },
        [post]
    );

    const logout = useCallback(async () => {
        try {
            await post(`${baseUrl}/logout/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated
            });
            navigate('/my-account/register');
            return true;
        } catch (error) {
            console.error('Error during logout:', error);
            return false;
        }
    }, [post, navigate, isAuthenticated]);

    const deleteUser = useCallback(async () => {
        try {
            const result = await del(`${baseUrl}/delete/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated
            });
            return result;
        } catch (error) {
            console.error('Error deleting user:', error);
            return undefined;
        }
    }, [del, isAuthenticated]);

    return {
        register,
        login,
        logout,
        deleteUser
    };
};

// Legacy exports for backward compatibility - will be removed in future versions
export const useRegister = () => {
    const { register } = useAuthentication();
    return { register };
};

export const useLogin = () => {
    const { login } = useAuthentication();
    return { login };
};

export const useLogout = () => {
    const { logout } = useAuthentication();
    return { logout };
};

export const useDelete = () => {
    const { deleteUser } = useAuthentication();
    return { deleteUser };
};

// Legacy photo exports - moved to usePhotoApi.js
export const useUploadPhoto = () => {
    console.warn(
        'useUploadPhoto is deprecated. Use usePhoto from usePhotoApi.js instead.'
    );
    const { uploadPhoto } = usePhoto();
    return { upload: uploadPhoto };
};

export const useGetPhoto = () => {
    console.warn(
        'useGetPhoto is deprecated. Use usePhoto from usePhotoApi.js instead.'
    );
    const { getPhoto } = usePhoto();
    return { getPhoto };
};

// Legacy profile exports - moved to useProfileApi.js
export const useGetPersonalInfo = () => {
    console.warn(
        'useGetPersonalInfo is deprecated. Use useProfile from useProfileApi.js instead.'
    );
    const { getPersonalInfo } = useProfile();
    return { getPersonalInfo };
};

export const useUpdatePersonalInfo = () => {
    console.warn(
        'useUpdatePersonalInfo is deprecated. Use useProfile from useProfileApi.js instead.'
    );
    const { updatePersonalInfo } = useProfile();
    return { updatePersonalInfo };
};

export const useChangePassword = () => {
    console.warn(
        'useChangePassword is deprecated. Use useProfile from useProfileApi.js instead.'
    );
    const { changePassword } = useProfile();
    return { changePassword };
};
