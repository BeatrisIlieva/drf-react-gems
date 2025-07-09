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
                        Your order should arrive in two business days if placed by 3PM ET on
                        weekdays or if placed by 12PM ET on Saturday. Orders placed on Sunday should
                        arrive on Wednesday.{' '}
                    </p>
                </section>
            </Popup>
        </>
    );
};
