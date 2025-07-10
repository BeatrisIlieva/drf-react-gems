import { useCallback, useEffect, useState } from 'react';

import { useNavigate } from 'react-router';

import { ShadowBox } from '../../../reusable/shadow-box/ShadowBox';

import { useProfile } from '../../../../api/useProfileApi';

import { useUserContext } from '../../../../contexts/UserContext';

import styles from './ShippingInformation.module.scss';

export const ShippingInformation = () => {
    const { email } = useUserContext();
    const { getPersonalInfo } = useProfile();
    const navigate = useNavigate();

    const [deliveryInfo, setDeliveryInfo] = useState(null);

    useEffect(() => {
        getPersonalInfo()
            .then(data => {
                if (data && !data.error) {
                    setDeliveryInfo(data);
                } else {
                    console.error('Failed to fetch delivery information:', data.error);
                }
            })
            .catch(error => {
                console.error('Error fetching delivery information:', error);
            });
    }, [getPersonalInfo, setDeliveryInfo, email]);

    const navigateBackToCheckoutPageHandler = useCallback(() => {
        navigate('/user/checkout');
    }, [navigate]);

    return (
        <ShadowBox title="Shipping Information" className={styles['shipping-information']}>
            <button className={styles['edit-button']} onClick={navigateBackToCheckoutPageHandler}>
                Edit
            </button>
            {deliveryInfo && (
                <>
                    <div className={styles['flex-wrapper']}>
                        <p className={styles['bolded']}>Email</p>
                        <p className={styles['subtle']}>{email}</p>
                    </div>
                    <div className={styles['flex-wrapper']}>
                        <p className={styles['bolded']}>Phone Number</p>
                        <p className={styles['subtle']}>{deliveryInfo.phoneNumber}</p>
                    </div>
                    <div className={styles['flex-wrapper']}>
                        <p className={styles['bolded']}>Shipping Address</p>
                        <p className={styles['subtle']}>Country: {deliveryInfo.country}</p>
                        <p className={styles['subtle']}>City: {deliveryInfo.city}</p>
                        <p className={styles['subtle']}>Zip Code: {deliveryInfo.zipCode}</p>
                        <p className={styles['subtle']}>
                            Street Address:
                            {deliveryInfo.streetAddress}
                        </p>
                        {deliveryInfo.apartment && (
                            <p className={styles['subtle']}>
                                Apartment:
                                {deliveryInfo.apartment}
                            </p>
                        )}
                    </div>
                </>
            )}
        </ShadowBox>
    );
};
