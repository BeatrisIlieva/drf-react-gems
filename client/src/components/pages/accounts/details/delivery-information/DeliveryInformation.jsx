import { useState, useEffect, useCallback } from 'react';
import { useUserAddress } from '../../../../../api/accounts/userAddressApi';
import { AddressFormModal } from './AddressFormModal';
import styles from './DeliveryInformation.module.scss';

export const DeliveryInformation = () => {
    const [addressData, setAddressData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const { getUserAddress } = useUserAddress();

    const loadAddressData = useCallback(async () => {
        setLoading(true);
        try {
            const result = await getUserAddress();
            setAddressData(result || null);
        } catch {
            setAddressData(null);
        } finally {
            setLoading(false);
        }
    }, [getUserAddress]);

    useEffect(() => {
        loadAddressData();
    }, [loadAddressData]);

    const handleAddAddress = () => {
        setShowModal(true);
    };

    const handleCloseModal = () => {
        setShowModal(false);
    };

    const handleSaveAddress = () => {
        loadAddressData();
    };

    const hasAddress = addressData && (
        addressData.state || 
        addressData.city || 
        addressData.streetAddress || 
        addressData.zipCode
    );

    return (
        <div className={styles.addressBook}>
            <h3>ADDRESS BOOK</h3>

            {loading ? (
                <div className={styles.loading}>
                    Loading address information...
                </div>
            ) : hasAddress ? (
                <div className={styles.addressCard}>
                    <div className={styles.addressName}>B11</div>
                    <div className={styles.addressDetails}>
                        {addressData.streetAddress?.streetAddress && `${addressData.streetAddress.streetAddress}, `}
                        {addressData.city?.name && `${addressData.city.name}, `}
                        {addressData.state?.name && `${addressData.state.name} `}
                        {addressData.zipCode?.zipCode}
                        {addressData.apartment && (
                            <>
                                <br />
                                Apt {addressData.apartment}
                            </>
                        )}
                    </div>
                    <div className={styles.phoneNumber}>(121) 755-5555</div>
                    
                    <div className={styles.addressActions}>
                        <div className={styles.defaultBadge}>
                            <div className={styles.checkIcon}></div>
                            DEFAULT
                        </div>
                        <button className={styles.actionButton} onClick={handleAddAddress}>
                            EDIT
                        </button>
                        <button className={styles.actionButton}>
                            REMOVE
                        </button>
                    </div>

                    <div className={styles.locationIcon}>📍</div>
                </div>
            ) : (
                <div className={styles.emptyState}>
                    <div className={styles.emptyIcon}>📦</div>
                    <p className={styles.emptyText}>No saved addresses</p>
                </div>
            )}

            <button 
                className={styles.addButton}
                onClick={handleAddAddress}
            >
                ADD A NEW ADDRESS
            </button>

            <AddressFormModal
                isOpen={showModal}
                onClose={handleCloseModal}
                onSave={handleSaveAddress}
            />
        </div>
    );
};
