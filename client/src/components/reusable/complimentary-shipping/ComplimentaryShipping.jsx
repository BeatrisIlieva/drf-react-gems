import { useState } from 'react';

import { Popup } from '../popup/Popup';
import { TruckIcon } from '../truck-icon/TruckIncon';

import styles from './ComplimentaryShipping.module.scss';

export const ComplimentaryShipping = () => {
    const [isPopupOpen, setIsPopupOpen] = useState(false);

    return (
        <>
            <button
                className={styles['complimentary-shipping']}
                onClick={() => setIsPopupOpen(true)}
            >
                <TruckIcon />
                <span>Complimentary 2-day shipping</span>
            </button>
            <Popup isOpen={isPopupOpen} onClose={() => setIsPopupOpen(false)}>
                <section className={styles['content']}>
                    <h4>Complimentary Two-Day Shipping</h4>
                    <p>
                        Your order will be completed within two days of being placed—no matter which day you order. We’re always working to get your gems to you as quickly as possible!
                    </p>
                </section>
            </Popup>
        </>
    );
};
