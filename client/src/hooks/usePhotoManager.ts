import { useState, useEffect, useCallback } from 'react';
import {
    useDetail,
    useGetPhoto,
    useUploadPhoto
} from '../api/authApi';

interface UsePhotoManagerReturn {
    currentPhoto: string | null;
    isLoading: boolean;
    isUploading: boolean;
    error: string | null;
    uploadPhoto: (file: File) => Promise<void>;
    refreshPhoto: () => Promise<void>;
}

export const usePhotoManager = (): UsePhotoManagerReturn => {
    const [currentPhoto, setCurrentPhoto] = useState<
        string | null
    >(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const { detail } = useDetail();
    const { upload } = useUploadPhoto();
    const { getPhoto } = useGetPhoto();

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
        async (file: File) => {
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
                // Load user details for authentication validation
                await detail();
                // Load current photo
                await refreshPhoto();
            } catch (err) {
                setError('Failed to initialize user data');
                console.error('Error initializing data:', err);
            }
        };

        initializeData();
    }, [detail, refreshPhoto]);

    return {
        currentPhoto,
        isLoading,
        isUploading,
        error,
        uploadPhoto,
        refreshPhoto
    };
};
