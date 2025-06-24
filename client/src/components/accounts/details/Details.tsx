import React, { useEffect, useState } from 'react';

import { Delete } from '../delete/Delete';
import { useDetail, useGetPhoto, useUploadPhoto } from '../../../api/authApi';
import { Logout } from '../logout/Logout';

export const Details: React.FC = () => {
    const { detail } = useDetail();
    const { upload } = useUploadPhoto();
    const { getPhoto } = useGetPhoto();
    const [photo, setPhoto] = useState<string | null>(null);

    useEffect(() => {
        // Load user details
        detail().then(() => {
            // We're not using the user data for display in this component yet
            // But the API call is still necessary for authentication validation
        });

        // Get user photo
        getPhoto().then((response) => {
            if (response?.photo_url) {
                setPhoto(response.photo_url);
            }
        });
    }, [detail, getPhoto]);

    const [image, setImage] = useState<File | null>(null);
    const [preview, setPreview] = useState<string | null>(null);
    const [uploadedImageUrl, setUploadedImageUrl] = useState<string>('');

    const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];
            setImage(file);
            setPreview(URL.createObjectURL(file));
        }
    };

    const handleUpload = async () => {
        if (!image) return;

        const formData = new FormData();
        formData.append('photo', image);

        const response = await upload(formData);
        if (response?.url) {
            setUploadedImageUrl(response.url);
        }
    };

    return (
        <>
            <Logout />
            <Delete />
            {photo && <img src={photo} alt="User profile" />}
            <div>
                <input type='file' onChange={handleImageChange} />
                {preview && <img src={preview} alt='Preview' style={{ width: 200 }} />}
                <button onClick={handleUpload}>Upload</button>
                {uploadedImageUrl && (
                    <p>
                        Image uploaded to: <a href={uploadedImageUrl}>{uploadedImageUrl}</a>
                    </p>
                )}
            </div>
        </>
    );
};
