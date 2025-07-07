import { Icon } from '../../../reusable/icon/Icon';

import styles from './Buttons.module.scss';
import { Link } from 'react-router';

import { useShoppingBagContext } from '../../../../contexts/ShoppingBagContext';
import { useWishlistContext } from '../../../../contexts/WishlistContext';
import { useAuth } from '../../../../hooks/auth/useAuth';
import { useEffect } from 'react';

export const Buttons = () => {
    const { isAuthenticated } = useAuth();
    const { shoppingBagItemsCount, updateShoppingBagCount } =
        useShoppingBagContext();
    const { wishlistItemsCount, updateWishlistCount } =
        useWishlistContext();

    useEffect(() => {
        updateShoppingBagCount();
        updateWishlistCount();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

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
                <Link to='/user/wishlist'>
                    <Icon name={'heart'} />
                    {wishlistItemsCount > 0 && (
                        <span>
                            <span>{wishlistItemsCount}</span>
                        </span>
                    )}
                </Link>
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
