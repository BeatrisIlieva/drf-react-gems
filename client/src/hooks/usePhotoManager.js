import { useCallback, useEffect, useState } from 'react';

import { usePhoto } from '../api/usePhotoApi';

export const usePhotoManager = () => {
    const [currentPhoto, setCurrentPhoto] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState(null);

    const { uploadPhoto, getPhoto, deletePhoto } = usePhoto();

    const deletePhotoHandler = useCallback(async () => {
        try {
            setIsLoading(true);
            setError(null);

            await deletePhoto();

            setCurrentPhoto(null);
        } catch (err) {
            setError('Failed to delete profile photo');
            console.error('Error deleting photo:', err);
        } finally {
            setIsLoading(false);
        }
    }, [deletePhoto]);

    const refreshPhoto = useCallback(async () => {
        try {
            setIsLoading(true);
            setError(null);

            const response = await getPhoto();
            if (response?.photoUrl) {
                setCurrentPhoto(response.photoUrl);
            }
        } catch (err) {
            setError('Failed to load profile photo');
            console.error('Error loading photo:', err);
        } finally {
            setIsLoading(false);
        }
    }, [getPhoto]);

    const uploadPhotoHandler = useCallback(
        async file => {
            try {
                setIsUploading(true);
                setError(null);

                const formData = new FormData();
                formData.append('photo', file);

                const response = await uploadPhoto(formData);
                if (response?.photoUrl) {
                    setCurrentPhoto(response.photoUrl);
                } else {
                    throw new Error('Upload failed - no URL returned');
                }
            } catch (err) {
                setError('Failed to upload photo');
                console.error('Error uploading photo:', err);
            } finally {
                setIsUploading(false);
            }
        },
        [uploadPhoto]
    );

    useEffect(() => {
        const initializeData = async () => {
            try {
                await refreshPhoto();
            } catch (err) {
                setError('Failed to initialize user data');
                console.error('Error initializing data:', err);
            }
        };

        initializeData();
    }, [refreshPhoto]);

    return {
        currentPhoto,
        isLoading,
        isUploading,
        error,
        uploadPhotoHandler,
        deletePhotoHandler,
    };
};
