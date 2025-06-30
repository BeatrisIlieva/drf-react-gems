import React from 'react';
import { ProfilePhotoUpload } from './profile-photo-upload/ProfilePhotoUpload';
import { usePhotoManager } from '../../../../hooks/usePhotoManager';
import { PersonalInfoForm } from './personal-info-form/PersonalInfoForm';
import { LoginInformation } from './login-information/LoginInformation';
import styles from './Details.module.scss';

export const Details: React.FC = () => {
    const { currentPhoto, isUploading, uploadPhoto } =
        usePhotoManager();

    return (
        <section className={styles['details']}>
            <section className={styles['photo']}>
                <h4>Profile Photo</h4>

                <ProfilePhotoUpload
                    currentPhoto={currentPhoto}
                    onPhotoUpdate={uploadPhoto}
                    isUploading={isUploading}
                />
            </section>
            <h2>Account Details</h2>
            <PersonalInfoForm />
            <LoginInformation />
        </section>
    );
};
