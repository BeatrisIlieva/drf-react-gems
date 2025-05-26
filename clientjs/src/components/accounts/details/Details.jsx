import { Logout } from '../logout/Logout';
import { useEffect, useState } from 'react';
import { useDetail, useGetPhoto, useUploadPhoto } from '../../../api/authApi';

import { Delete } from '../delete/Delete';

export const Details = () => {
    const [user, setUser] = useState([]);
    const { detail } = useDetail();
    const { upload } = useUploadPhoto();
    const { getPhoto } = useGetPhoto();
    const [photo, setPhoto] = useState(null);

    useEffect(() => {
        detail().then((response) => setUser(response));
        getPhoto().then((response) => {setPhoto(response.photo_url)});
    }, [detail, getPhoto]);

    const [image, setImage] = useState(null);
    const [preview, setPreview] = useState(null);
    const [uploadedImageUrl, setUploadedImageUrl] = useState('');

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        setImage(file);
        setPreview(URL.createObjectURL(file));
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append('photo', image);

        const response = await upload(formData);
        setUploadedImageUrl(response.data.photo);
    };


    return (
        <>
            <Logout />
            <Delete />
            {photo && <img src={photo} />}
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
