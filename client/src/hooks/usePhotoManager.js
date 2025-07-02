import { useState, useEffect, useCallback } from 'react';
import { usePhoto } from '../api/accounts/usePhotoApi';

export const usePhotoManager = () => {
    const [currentPhoto, setCurrentPhoto] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState(null);

    const { uploadPhoto: upload, getPhoto } = usePhoto();

    const refreshPhoto = useCallback(async () => {
        try {
            setIsLoading(true);
            setError(null);

            const response = await getPhoto();
            if (response?.photo_url) {
                setCurrentPhoto(response.photo_url);
            }
        } catch (err) {
            setError('Failed to load profile photo');
            console.error('Error loading photo:', err);
        } finally {
            setIsLoading(false);
        }
    }, [getPhoto]);

    const uploadPhoto = useCallback(
        async (file) => {
            try {
                setIsUploading(true);
                setError(null);

                const formData = new FormData();
                formData.append('photo', file);

                const response = await upload(formData);
                if (response?.url) {
                    setCurrentPhoto(response.url);
                } else {
                    throw new Error(
                        'Upload failed - no URL returned'
                    );
                }
            } catch (err) {
                setError('Failed to upload photo');
                console.error('Error uploading photo:', err);
            } finally {
                setIsUploading(false);
            }
        },
        [upload]
    );

    useEffect(() => {
        const initializeData = async () => {
            try {
                // Load current photo
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
        uploadPhoto,
        refreshPhoto
    };
};
