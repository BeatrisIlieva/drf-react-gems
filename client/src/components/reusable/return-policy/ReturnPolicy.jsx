import { useState } from 'react';

import { Icon } from '../icon/Icon';
import { Popup } from '../popup/Popup';

import styles from './ReturnPolicy.module.scss';

export const ReturnPolicy = () => {
    const [isPopupOpen, setIsPopupOpen] = useState(false);

    return (
        <>
            <button className={styles['return-policy']} onClick={() => setIsPopupOpen(true)}>
                <Icon name={'calendar'} fontSize={0.9} isSubtle={true} />
                <span>Complimentary 30-day returns</span>
            </button>
            <Popup isOpen={isPopupOpen} onClose={() => setIsPopupOpen(false)}>
                <section className={styles['content']}>
                    <h3>Complimentary 30-day returns</h3>
                    <p>
                        We are pleased to offer a full refund for DRFReactGems.com purchases
                        returned within 30 days of their purchase date.
                    </p>
                    <p>
                        All refunds will be made to the purchaser and issued to the original form of
                        payment.
                    </p>
                    <p>
                        <span>Please note:</span> Returns must be accompanied by a sales receipt and
                        received unaltered, unworn and in sellable condition. Some exclusions may
                        apply. Used merchandise will not be accepted for refund or exchange unless
                        defective.
                    </p>
                </section>
            </Popup>
        </>
    );
};
