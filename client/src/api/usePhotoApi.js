import { useCallback } from 'react';

import { useApi } from '../hooks/useApi';
import { useAuth } from '../hooks/useAuth';

import { keysToCamelCase } from '../utils/convertToCamelCase';

import { HOST } from '../constants/host';

const baseUrl = `${HOST}/api/accounts/photo`;

export const usePhoto = () => {
    const { get, patch } = useApi();
    const { isAuthenticated } = useAuth();

    const getPhoto = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated,
            });

            return keysToCamelCase(response);
        } catch (error) {
            console.error(error);
        }
    }, [get, isAuthenticated]);

    const uploadPhoto = useCallback(
        async photoData => {
            try {
                const response = await patch(`${baseUrl}/`, {
                    data: photoData,
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated,
                    contentType: 'multipart/form-data',
                });

                return keysToCamelCase(response);
            } catch (error) {
                console.error(error);
            }
        },
        [patch, isAuthenticated]
    );

    const deletePhoto = useCallback(async () => {
        try {
            const formData = new FormData();
            formData.append('photo', '');

            const response = await patch(`${baseUrl}/`, {
                data: formData,
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated,
                contentType: 'multipart/form-data',
            });

            return keysToCamelCase(response);
        } catch (error) {
            console.error(error);
        }
    }, [patch, isAuthenticated]);

    return {
        getPhoto,
        uploadPhoto,
        deletePhoto,
    };
};
