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
                <span>Complimentary 1-day shipping</span>
            </button>
            <Popup isOpen={isPopupOpen} onClose={() => setIsPopupOpen(false)}>
                <section className={styles['content']}>
                    <h4>Complimentary One-Day Shipping</h4>
                    <p>
                        Your order will be completed within one day of being placed—no matter which
                        day you order. We’re always working to get your gems to you as quickly as
                        possible!
                    </p>
                </section>
            </Popup>
        </>
    );
};
