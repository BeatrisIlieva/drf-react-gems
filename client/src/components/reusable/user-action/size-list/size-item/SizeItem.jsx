import { useProductItemContext } from '../../../../../contexts/ProductItemContext';
import { useShoppingBagContext } from '../../../../../contexts/ShoppingBagContext';

import styles from './SizeItem.module.scss';

export const SizeItem = ({ item }) => {
    const { selectedSize, setSelectedSizeHandler, notSelectedSizeError } = useProductItemContext();
    const { shoppingBagItems } = useShoppingBagContext();

    const isSoldOut = shoppingBagItems.some(bagItem => {
        return (
            (bagItem.id === item.id || bagItem.inventory === item.id) &&
            bagItem.quantity === item.quantity
        );
    });

    return (
        <li className={styles['size-item']}>
            <button
                className={`${isSoldOut ? styles['sold-out'] : ''} ${
                    selectedSize === item.size.id ? styles['selected'] : ''
                } ${notSelectedSizeError === true ? styles['error'] : ''}`.trim()}
                disabled={isSoldOut}
                onClick={() => setSelectedSizeHandler(item.size.id, item.id)}
            >
                {item.size.name}
            </button>
        </li>
    );
};
