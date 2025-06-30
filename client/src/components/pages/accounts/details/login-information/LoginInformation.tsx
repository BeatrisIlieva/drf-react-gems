import { useState, useEffect, type ReactElement } from 'react';
import { useDetail } from '../../../../../api/authApi';
import { DetailsContainer } from '../details-container/DetailsContainer';
import { Popup } from '../../../../reusable/popup/Popup';
import { PasswordUpdateForm } from '../password-update-form/PasswordUpdateForm';
import { Icon } from '../../../../reusable/icon/Icon';
import styles from './LoginInformation.module.scss';

interface UserDetails {
    email?: string;
    username?: string;
}

export const LoginInformation = (): ReactElement => {
    const [userDetails, setUserDetails] = useState<UserDetails>(
        {}
    );
    const [isPasswordPopupOpen, setIsPasswordPopupOpen] =
        useState(false);
    const [loading, setLoading] = useState(true);

    const { detail } = useDetail();

    useEffect(() => {
        const loadUserDetails = async () => {
            try {
                const userInfo = await detail();
                if (userInfo) {
                    setUserDetails({
                        email: userInfo.email,
                        username: userInfo.username
                    });
                }
            } finally {
                setLoading(false);
            }
        };

        loadUserDetails();
    }, [detail]);

    if (loading) {
        return (
            <DetailsContainer>
                <h3>Login Information</h3>
                <div>Loading...</div>
            </DetailsContainer>
        );
    }

    return (
        <>
            <DetailsContainer>
                <h3>Login Information</h3>

                <div className={styles['login-information']}>
                    <div className={styles['user-info']}>
                        <div className={styles['column']}>
                            <div className={styles['info-group']}>
                                <div className={styles.label}>
                                    Email Address
                                </div>
                                <div className={styles.value}>
                                    {userDetails.email ||
                                        'Not available'}
                                    <Icon
                                        name='lock'
                                        fontSize={0.6}
                                    />
                                </div>
                            </div>

                            {userDetails.username && (
                                <div
                                    className={
                                        styles['info-group']
                                    }
                                >
                                    <div className={styles.label}>
                                        Username
                                    </div>
                                    <div className={styles.value}>
                                        {userDetails.username}
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
