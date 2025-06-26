import { useEffect, type ReactElement } from 'react';

import { Icon } from '../../../reusable/icon/Icon';

import styles from './Buttons.module.scss';
import { Link } from 'react-router';

import { useShoppingBagContext } from '../../../../contexts/ShoppingBagContext';
import { useWishlistContext } from '../../../../contexts/WishlistContext';
import { useAuth } from '../../../../hooks/auth/useAuth';

export const Buttons = (): ReactElement => {
    const { isAuthenticated } = useAuth();
    const { shoppingBagItemsCount, updateShoppingBagCount } =
        useShoppingBagContext();
    const { wishlistCount, updateWishlistCount } = useWishlistContext();

    useEffect(() => {
        updateShoppingBagCount();
        updateWishlistCount();
    }, [updateShoppingBagCount, updateWishlistCount]);

    return (
        <ul className={styles['buttons']}>
            <li>
                <Icon name={'search'} fontSize={0.7} />
                <span>Search</span>
            </li>

            <li>
                <Link
                    to={
                        isAuthenticated
                            ? '/my-account/details'
                            : '/my-account/login'
                    }
                >
                    <Icon name={'user'} fontSize={1} />
                    <span>1</span>
                </Link>
            </li>

            <li>
                <Icon name={'heart'} />
                {wishlistCount > 0 && (
                    <span>
                        <span>{wishlistCount}</span>
                    </span>
                )}
            </li>
            <li>
                <Link to='/user/shopping-bag'>
                    <Icon name={'bag'} />
                    {shoppingBagItemsCount > 0 && (
                        <span>
                            <span>{shoppingBagItemsCount}</span>
                        </span>
                    )}
                </Link>
            </li>
        </ul>
    );
};
