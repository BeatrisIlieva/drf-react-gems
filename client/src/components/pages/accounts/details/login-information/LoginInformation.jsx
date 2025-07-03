import { useState } from 'react';
import { DetailsContainer } from '../details-container/DetailsContainer';
import { Popup } from '../../../../reusable/popup/Popup';
import { PasswordUpdateForm } from '../password-update-form/PasswordUpdateForm';
import { Icon } from '../../../../reusable/icon/Icon';
import styles from './LoginInformation.module.scss';
import { useUserContext } from '../../../../../contexts/UserContext';

export const LoginInformation = () => {
    const [isPasswordPopupOpen, setIsPasswordPopupOpen] =
        useState(false);

    const { email, username } = useUserContext();

    return (
        <>
            <DetailsContainer title='Login Information'>
                <div className={styles['login-information']}>
                    <div className={styles['user-info']}>
                        <div className={styles['column']}>
                            <div className={styles['info-group']}>
                                <div className={styles.label}>
                                    Email Address
                                </div>
                                <div className={styles.value}>
                                    {email || 'Not available'}
                                    <Icon
                                        name='lock'
                                        fontSize={0.6}
                                    />
                                </div>
                            </div>

                            {username && (
                                <div
                                    className={
                                        styles['info-group']
                                    }
                                >
                                    <div className={styles.label}>
                                        Username
                                    </div>
                                    <div className={styles.value}>
                                        {username}
                                        <Icon
                                            name='lock'
                                            fontSize={0.6}
                                        />
                                    </div>
                                </div>
                            )}
                        </div>

                        <div className={styles['column']}>
                            <div className={styles['info-group']}>
                                <div className={styles.label}>
                                    Password
                                </div>
                                <div className={styles.value}>
                                    ••••••••
                                </div>
                            </div>
                            <button
                                className={
                                    styles['change-password-link']
                                }
                                onClick={() =>
                                    setIsPasswordPopupOpen(true)
                                }
                            >
                                Change Password
                            </button>
                        </div>
                    </div>
                </div>
            </DetailsContainer>

            <Popup
                isOpen={isPasswordPopupOpen}
                onClose={() => setIsPasswordPopupOpen(false)}
            >
                <PasswordUpdateForm
                    onSuccess={() =>
                        setIsPasswordPopupOpen(false)
                    }
                />
            </Popup>
        </>
    );
};
