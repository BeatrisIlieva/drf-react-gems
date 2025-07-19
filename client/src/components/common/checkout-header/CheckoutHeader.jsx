import { useLocation } from 'react-router';

import { Icon } from '../../reusable/icon/Icon';

import styles from './CheckoutHeader.module.scss';

export const CheckoutHeader = () => {
    const location = useLocation();

    const title = location.pathname.includes('payment') ? 'Payment' : 'Checkout';

    return (
        <header className={styles['checkout-header']}>
            <h2>{title}</h2>
            <div>
                <span className={`${title === 'Checkout' ? styles['active'] : ''}`.trim()}>
                    Shipping
                </span>
                <Icon name="arrowRight" isSubtle={true} fontSize={0.6} />
                <span className={`${title === 'Payment' ? styles['active'] : ''}`.trim()}>
                    Payment
                </span>
            </div>
        </header>
    );
};
