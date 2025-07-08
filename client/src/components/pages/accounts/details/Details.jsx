import { ProfilePhotoUpload } from './profile-photo-upload/ProfilePhotoUpload';
import { usePhotoManager } from '../../../../hooks/usePhotoManager';
import { DeliveryAddressForm } from './delivery-address-form/DeliveryAddressForm';
import { LoginInformation } from './login-information/LoginInformation';
import styles from './Details.module.scss';
import { DeleteButton } from '../../../reusable/delete-button/DeleteButton';
import { useState } from 'react';
import { Popup } from '../../../reusable/popup/Popup';
import { Deletion } from '../../../reusable/deletion/Deletion';
import { PaddedContainer } from '../../../reusable/padded-container/PaddedContainer';

export const Details = () => {
    const {
        currentPhoto,
        isUploading,
        uploadPhotoHandler,
        deletePhotoHandler
    } = usePhotoManager();

    const [
        isDeleteProfileImagePopupOpen,
        setIsDeleteProfileImagePopupOpen
    ] = useState(false);

    const confirmDeleteHandler = async () => {
        await deletePhotoHandler();
        setIsDeleteProfileImagePopupOpen(false);
    };

    return (
        <PaddedContainer>
            <section className={styles['details']}>
                <section className={styles['photo']}>
                    <h4>Profile Photo</h4>

                    <ProfilePhotoUpload
                        currentPhoto={currentPhoto}
                        onPhotoUpdate={uploadPhotoHandler}
                        isUploading={isUploading}
                    />

                    {currentPhoto && (
                        <DeleteButton
                            entityName='photo'
                            callbackHandler={() =>
                                setIsDeleteProfileImagePopupOpen(
                                    true
                                )
                            }
                        />
                    )}
                </section>
                <h2>Account Details</h2>
                <LoginInformation />
                <DeliveryAddressForm />

                <Popup
                    isOpen={isDeleteProfileImagePopupOpen}
                    onClose={() =>
                        setIsDeleteProfileImagePopupOpen(false)
                    }
                >
                    <Deletion
                        entityName='profile photo'
                        onProceed={confirmDeleteHandler}
                        onCancel={() =>
                            setIsDeleteProfileImagePopupOpen(
                                false
                            )
                        }
                    />
                </Popup>
            </section>
        </PaddedContainer>
    );
};
