import { TruckIcon } from '../truck-icon/TruckIncon';

import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';

import styles from './Delivery.module.scss';

export const Delivery = ({ fontSize }) => {
    const { shoppingBagItemsCount } = useShoppingBagContext();

    return (
        <p
            className={styles['delivery']}
            style={{
                fontSize: fontSize ? `${fontSize}em` : '1em',
            }}
        >
            <TruckIcon />
            <span>Delivery</span>
            <span>{`(${shoppingBagItemsCount} ${
                shoppingBagItemsCount > 1 ? 'items' : 'item'
            })`}</span>
        </p>
    );
};
