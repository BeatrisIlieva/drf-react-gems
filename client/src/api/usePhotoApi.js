import { useCallback } from 'react';

import { useApi } from '../hooks/useApi';

import { keysToCamelCase } from '../utils/convertToCamelCase';

import { HOST } from '../constants/host';

const baseUrl = `${HOST}/api/accounts/photo`;

export const usePhoto = () => {
    const { get, patch } = useApi();

    const getPhoto = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}/`, {
                accessRequired: true,
                refreshRequired: true,
            });

            return keysToCamelCase(response);
        } catch (error) {
            console.error(error);
        }
    }, [get]);

    const uploadPhoto = useCallback(
        async photoData => {
            try {
                const response = await patch(`${baseUrl}/`, {
                    data: photoData,
                    accessRequired: true,
                    refreshRequired: true,
                    contentType: 'multipart/form-data',
                });

                return keysToCamelCase(response);
            } catch (error) {
                console.error(error);
            }
        },
        [patch]
    );

    const deletePhoto = useCallback(async () => {
        try {
            const formData = new FormData();
            formData.append('photo', '');

            const response = await patch(`${baseUrl}/`, {
                data: formData,
                accessRequired: true,
                refreshRequired: true,
                contentType: 'multipart/form-data',
            });

            return keysToCamelCase(response);
        } catch (error) {
            console.error(error);
        }
    }, [patch]);

    return {
        getPhoto,
        uploadPhoto,
        deletePhoto,
    };
};
