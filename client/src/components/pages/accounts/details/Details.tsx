import React from 'react';
import { ProfilePhotoUpload } from './profile-photo-upload/ProfilePhotoUpload';
import { usePhotoManager } from '../../../../hooks/usePhotoManager';
import styles from './Details.module.scss';
import { PersonalInfoForm } from './personal-info-form/PersonalInfoForm';


export const Details: React.FC = () => {
    const { currentPhoto, isLoading, isUploading, uploadPhoto } =
        usePhotoManager();

    return (
        <section className={styles['details']}>
            <section className={styles['photo']}>
                <h4>
                    Profile Photo
                </h4>

                <ProfilePhotoUpload
                    currentPhoto={currentPhoto}
                    onPhotoUpdate={uploadPhoto}
                    isUploading={isUploading}
                />
            </section>
            <PersonalInfoForm/>
        </section>
    );
};
