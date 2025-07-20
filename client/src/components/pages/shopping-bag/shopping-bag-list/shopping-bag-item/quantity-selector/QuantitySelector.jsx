import { useEffect, useState } from 'react';

import { Icon } from '../../../../../reusable/icon/Icon';

import { useShoppingBag } from '../../../../../../api/shoppingBagApi';

import { useShoppingBagContext } from '../../../../../../contexts/ShoppingBagContext';
import { useUserContext } from '../../../../../../contexts/UserContext';

import styles from './QuantitySelector.module.scss';

export const QuantitySelector = ({ quantity, id, inventory, availableQuantity }) => {
    const { updateItem } = useShoppingBag();
    const { refreshShoppingBag } = useShoppingBagContext();
    const [isUpdating, setIsUpdating] = useState(false);
    const [localQuantity, setLocalQuantity] = useState(quantity);
    const { id: userId } = useUserContext();

    useEffect(() => {
        setLocalQuantity(quantity);
    }, [quantity]);

    const handleQuantityChange = async newQuantity => {
        if (newQuantity === localQuantity) return;

        setIsUpdating(true);
        try {
            if (userId) {
                await updateItem({
                    inventory,
                    quantity: newQuantity,
                    id,
                });
            }
            setLocalQuantity(newQuantity);
            if (userId) {
                refreshShoppingBag();
            } else {
                refreshShoppingBag(id, newQuantity);
            }
        } catch (err) {
            console(err.message);
            setLocalQuantity(quantity);
        } finally {
            setIsUpdating(false);
        }
    };

    const incrementQuantity = () => {
        handleQuantityChange(localQuantity + 1);
    };

    const decrementQuantity = () => {
        if (localQuantity > 1) {
            handleQuantityChange(localQuantity - 1);
        } else {
            handleQuantityChange(0);
            setTimeout(() => {
                if (userId) {
                    refreshShoppingBag();
                } else {
                    refreshShoppingBag(id, 0);
                }
            }, 100);
        }
    };

    return (
        <span className={styles['quantity-selector']}>
            <button onClick={decrementQuantity} disabled={isUpdating}>
                <Icon name="minus" />
            </button>
            <span>{localQuantity}</span>
            <button
                onClick={incrementQuantity}
                disabled={isUpdating || localQuantity >= availableQuantity}
            >
                <Icon name="plus" />
            </button>
            {isUpdating && <span className={styles['updating-indicator']}>Updating...</span>}
        </span>
    );
};
