import { useCallback } from 'react';
import { useApi } from '../../hooks/useApi';
import { HOST } from '../../constants/host';
import { useAuth } from '../../hooks/auth/useAuth';

const baseUrl = `${HOST}/api/accounts/address`;

export const useUserAddress = () => {
    const { get, patch, del } = useApi();
    const { isAuthenticated } = useAuth();

    const getUserAddress = useCallback(async () => {
        try {
            const result = await get(`${baseUrl}/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated
            });
            return result;
        } catch {
            return undefined;
        }
    }, [get, isAuthenticated]);

    const updateUserAddress = useCallback(async (addressData) => {
        try {
            const result = await patch(`${baseUrl}/`, {
                data: addressData,
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated
            });
            return result;
        } catch {
            return undefined;
        }
    }, [patch, isAuthenticated]);

    const deleteUserAddress = useCallback(async () => {
        try {
            await del(`${baseUrl}/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated
            });
            return true;
        } catch {
            return false;
        }
    }, [del, isAuthenticated]);

    const getStates = useCallback(async () => {
        try {
            const result = await get(`${baseUrl}/states/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated
            });
            return result;
        } catch {
            return [];
        }
    }, [get, isAuthenticated]);

    const getCities = useCallback(async (stateId) => {
        try {
            const url = stateId ? `${baseUrl}/cities/?state_id=${stateId}` : `${baseUrl}/cities/`;
            const result = await get(url, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated
            });
            return result;
        } catch {
            return [];
        }
    }, [get, isAuthenticated]);

    const getZipCodes = useCallback(async (cityId) => {
        try {
            const url = cityId ? `${baseUrl}/zip-codes/?city_id=${cityId}` : `${baseUrl}/zip-codes/`;
            const result = await get(url, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated
            });
            return result;
        } catch {
            return [];
        }
    }, [get, isAuthenticated]);

    const getStreetAddresses = useCallback(async (zipCodeId) => {
        try {
            const url = zipCodeId ? `${baseUrl}/street-addresses/?zip_code_id=${zipCodeId}` : `${baseUrl}/street-addresses/`;
            const result = await get(url, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated
            });
            return result;
        } catch {
            return [];
        }
    }, [get, isAuthenticated]);

    return {
        getUserAddress,
        updateUserAddress,
        deleteUserAddress,
        getStates,
        getCities,
        getZipCodes,
        getStreetAddresses,
    };
};
