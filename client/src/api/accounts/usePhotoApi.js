import { useCallback } from 'react';
import { useBaseApi } from '../../hooks/useBaseApi';
import { HOST } from '../../constants/host';

const baseUrl = `${HOST}/accounts/photo`;

export const usePhoto = () => {
    const { get, patch } = useBaseApi(baseUrl, {
        requireAuth: true
    });

    const getPhoto = useCallback(async () => {
        return await get();
    }, [get]);

    const uploadPhoto = useCallback(
        async (photoData) => {
            return await patch('', photoData, {
                contentType: 'multipart/form-data'
            });
        },
        [patch]
    );

    const deletePhoto = useCallback(async () => {
        return await patch('', { photo: null });
    }, [patch]);

    return {
        getPhoto,
        uploadPhoto,
        deletePhoto
    };
};
