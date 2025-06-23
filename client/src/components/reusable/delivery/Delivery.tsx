import React from 'react';
import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';
import { TruckIcon } from '../truck-icon/TruckIncon';

import styles from './Delivery.module.scss';

interface DeliveryProps {
    fontSize: 'large' | string;
}

export const Delivery: React.FC<DeliveryProps> = ({
    fontSize
}) => {
    const { shoppingBagItemsCount } = useShoppingBagContext();

    return (
        <p
            className={`${styles['delivery']} ${styles[fontSize]}`}
        >
            <TruckIcon />
            <span>Delivery</span>
            <span>{`(${shoppingBagItemsCount} ${
                shoppingBagItemsCount > 1 ? 'items' : 'item'
            })`}</span>
        </p>
    );
};
