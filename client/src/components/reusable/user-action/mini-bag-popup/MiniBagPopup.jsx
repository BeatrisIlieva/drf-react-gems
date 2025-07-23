import { useEffect } from 'react';

import { useNavigate } from 'react-router';

import { ShoppingBagItem } from '../../../pages/shopping-bag/shopping-bag-list/shopping-bag-item/ShoppingBagItem';
import { Button } from '../../button/Button';
import { Popup } from '../../popup/Popup';

import { useShoppingBagContext } from '../../../../contexts/ShoppingBagContext';

import { formatPrice } from '../../../../utils/formatPrice';

import styles from './MiniBagPopup.module.scss';

export const MiniBagPopup = ({ isOpen, onClose }) => {
    const navigate = useNavigate();
    const {
        shoppingBagItems,
        shoppingBagItemsCount,
        shoppingBagTotalPrice,
        continueCheckoutHandler,
    } = useShoppingBagContext();

    // useEffect(() => {
    //     if (shoppingBagItemsCount === 0 && isOpen) {
    //         onClose();
    //     }
    // }, [shoppingBagItemsCount, isOpen, onClose]);

    const navigateToShoppingBag = () => {
        navigate('/user/shopping-bag');
        onClose();
    };

    return (
        <Popup isOpen={isOpen} onClose={onClose}>
            <div className={styles['mini-bag-header']}>
                <h3>Your Bag</h3>
                <span>
                    {shoppingBagItemsCount} {shoppingBagItemsCount > 1 ? 'items' : 'item'}
                </span>
            </div>

            <ul className={styles['shopping-bag-list']}>
                {shoppingBagItems.map(item => (
                    <ShoppingBagItem key={item.id} {...item} />
                ))}
            </ul>

            <div className={styles['total-price-wrapper']}>
                <span>Total</span>
                <span>{formatPrice(shoppingBagTotalPrice)}</span>
            </div>

            <div className={styles['mini-bag-buttons-wrapper']}>
                <Button
                    title="View Bag"
                    color="white"
                    buttonGrow="1"
                    callbackHandler={navigateToShoppingBag}
                />
                <Button
                    title="Continue Checkout"
                    color="black"
                    buttonGrow="1"
                    callbackHandler={continueCheckoutHandler}
                />
            </div>
        </Popup>
    );
};
