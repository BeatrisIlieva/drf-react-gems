import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';
import { TruckIcon } from '../truck-icon/TruckIncon';

import styles from './Delivery.module.css';

export const Delivery = ({ fontSize }) => {
    const { shoppingBagItemsCount } = useShoppingBagContext();

    return (
        <p className={`${styles['delivery']} ${styles[fontSize]}`}>
            <TruckIcon />
            <span>Delivery</span>
            <span>{`(${shoppingBagItemsCount} ${
                shoppingBagItemsCount > 1 ? 'items' : 'item'
            })`}</span>
        </p>
    );
};
