import { useState } from 'react';

import { DeleteButton } from '../../../../reusable/delete-button/DeleteButton';
import { Deletion } from '../../../../reusable/deletion/Deletion';
import { Icon } from '../../../../reusable/icon/Icon';
import { PasswordUpdateForm } from './password-update-form/PasswordUpdateForm';
import { Popup } from '../../../../reusable/popup/Popup';
import { ShadowBox } from '../../../../reusable/shadow-box/ShadowBox';

import { useAuthentication } from '../../../../../api/authApi';

import { useUserContext } from '../../../../../contexts/UserContext';

import styles from './LoginInformation.module.scss';

export const LoginInformation = () => {
    const { userLogoutHandler } = useUserContext();
    const { deleteUser } = useAuthentication();
    const { email, username } = useUserContext();

    const [isPasswordPopupOpen, setIsPasswordPopupOpen] = useState(false);
    const [isDeleteAccountPopupOpen, setIsDeleteAccountPopupOpen] = useState(false);

    const deleteHandler = async () => {
        await deleteUser();
        setIsDeleteAccountPopupOpen(false);
        userLogoutHandler();
    };

    return (
        <>
            <ShadowBox title="Login Information">
                <div className={styles['login-information']}>
                    <div className={styles['user-info']}>
                        <div className={styles['column']}>
                            <div className={styles['info-group']}>
                                <div className={styles['label']}>Email Address</div>
                                <div className={styles['value']}>
                                    {email || 'Not available'}
                                    <Icon name="lock" fontSize={0.6} />
                                </div>
                            </div>

                            {username && (
                                <div className={styles['info-group']}>
                                    <div className={styles['label']}>Username</div>
                                    <div className={styles['value']}>
                                        {username}
                                        <Icon name="lock" fontSize={0.6} />
                                    </div>
                                </div>
                            )}
                        </div>

                        <div className={styles['column']}>
                            <button
                                className={styles['change-password-link']}
                                onClick={() => setIsPasswordPopupOpen(true)}
                            >
                                Change Password
                            </button>
                            <DeleteButton
                                callbackHandler={() => setIsDeleteAccountPopupOpen(true)}
                                entityName="account"
                            />
                        </div>
                    </div>
                </div>
            </ShadowBox>

            <Popup isOpen={isPasswordPopupOpen} onClose={() => setIsPasswordPopupOpen(false)}>
                <PasswordUpdateForm onSuccess={() => setIsPasswordPopupOpen(false)} />
            </Popup>
            <Popup
                isOpen={isDeleteAccountPopupOpen}
                onClose={() => setIsDeleteAccountPopupOpen(false)}
            >
                <Deletion
                    entityName="account"
                    onProceed={deleteHandler}
                    onCancel={() => setIsDeleteAccountPopupOpen(false)}
                />
            </Popup>
        </>
    );
};
