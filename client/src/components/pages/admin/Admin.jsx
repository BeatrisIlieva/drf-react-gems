import { useCallback, useEffect, useState } from 'react';

import { Button } from '../../reusable/button/Button';
import { PaddedContainer } from '../../reusable/padded-container/PaddedContainer';
import { Logout } from '../accounts/logout/Logout';

import { useAdmin } from '../../../api/adminApi';

import { formatPrice } from '../../../utils/formatPrice';

import styles from './Admin.module.scss';

export const AdminPage = () => {
    const { sendReminder, getBagReminderInfo } = useAdmin();
    const [bagInfo, setBagInfo] = useState([]);
    const [emailsSentSuccessfully, setEmailsSentSuccessfully] = useState(false);

    const fetchBagInfo = useCallback(async () => {
        const data = await getBagReminderInfo();

        if (data) setBagInfo(data);
    }, [getBagReminderInfo]);

    useEffect(() => {
        fetchBagInfo();
    }, [fetchBagInfo]);

    const handleSendReminder = async () => {
        const result = await sendReminder();

        setEmailsSentSuccessfully(result.success);
    };

    const formatDate = dateString => {
        const date = new Date(dateString);
        const options = {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        };

        return date.toLocaleDateString('en-US', options);
    };

    return (
        <PaddedContainer>
            <section className={styles['admin']}>
                <header>
                    <h2>Shopping Bags Older Than One Day</h2>
                    <Logout />
                </header>

                {bagInfo && bagInfo.length > 0 ? (
                    <>
                        <div className={styles['button-wrapper']}>
                            <Button
                                title="Send Cart Reminder Emails"
                                color="black"
                                width={20}
                                callbackHandler={handleSendReminder}
                            />
                            {emailsSentSuccessfully && <p>Emails have been sent successfully</p>}
                        </div>

                        <div className={styles['bag-info-container']}>
                            <div className={styles['grid-header']}>
                                <div>ID</div>
                                <div>Created At</div>
                                <div>User Email</div>
                                <div>Quantity</div>
                                <div>Total Price</div>
                                <div>Product Info</div>
                            </div>
                            <div className={styles['grid-items']}>
                                {bagInfo.map(item => (
                                    <div key={item.id} className={styles['grid-item']}>
                                        <div className={styles['item-row']}>
                                            <span className={styles['item-label']}>ID</span>
                                            <span className={styles['item-value id-value']}>
                                                {item.id}
                                            </span>
                                        </div>
                                        <div className={styles['item-row']}>
                                            <span className={styles['item-label']}>Created At</span>
                                            <span className={styles['item-value']}>
                                                {formatDate(item.created_at)}
                                            </span>
                                        </div>
                                        <div className={styles['item-row']}>
                                            <span className={styles['item-label']}>User Email</span>
                                            <span className={styles['item-value email-value']}>
                                                {item.user_email}
                                            </span>
                                        </div>
                                        <div className={styles['item-row']}>
                                            <span className={styles['item-label']}>Quantity</span>
                                            <span className={styles['item-value quantity-value']}>
                                                {item.quantity}
                                            </span>
                                        </div>
                                        <div className={styles['item-row']}>
                                            <span className={styles['item-label']}>
                                                Total Price
                                            </span>
                                            <span className={styles['item-value price-value']}>
                                                {formatPrice(item.total_price)}
                                            </span>
                                        </div>
                                        <div className={styles['item-row']}>
                                            <span className={styles['item-label']}>
                                                Product Info
                                            </span>
                                            <span className={styles['item-value']}>
                                                {item.product_info}
                                            </span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </>
                ) : (
                    <p>No abandoned shopping bags found</p>
                )}
            </section>
        </PaddedContainer>
    );
};
