import { Link } from 'react-router';

import { faClipboardUser } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import { Icon } from '../../../reusable/icon/Icon';

import { useAuth } from '../../../../hooks/useAuth';

import { useShoppingBagContext } from '../../../../contexts/ShoppingBagContext';
import { useWishlistContext } from '../../../../contexts/WishlistContext';

import styles from './Buttons.module.scss';

export const Buttons = () => {
    const { isAuthenticated } = useAuth();
    const { shoppingBagItemsCount } = useShoppingBagContext();
    const { wishlistItemsCount } = useWishlistContext();

    const { permissions } = useAuth();
    const isReviewer = permissions?.includes('products.approve_review');

    return (
        <ul className={styles['buttons']}>
            {isReviewer ? (
                <li>
                    <Link to="/admin-page" className={styles['admin-icon']}>
                        <FontAwesomeIcon icon={faClipboardUser} />
                    </Link>
                </li>
            ) : (
                <>
                    <li>
                        <Link to={isAuthenticated ? '/my-account/details' : '/my-account/login'}>
                            <Icon name={'user'} fontSize={1} />
                            {isAuthenticated && <span></span>}
                        </Link>
                    </li>

                    <li>
                        <Link to="/user/wishlist">
                            <Icon name={'heart'} />
                            {wishlistItemsCount > 0 && (
                                <span>
                                    <span>{wishlistItemsCount}</span>
                                </span>
                            )}
                        </Link>
                    </li>
                    <li>
                        <Link to="/user/shopping-bag">
                            <Icon name={'bag'} />
                            {shoppingBagItemsCount > 0 && (
                                <span>
                                    <span>{shoppingBagItemsCount}</span>
                                </span>
                            )}
                        </Link>
                    </li>
                </>
            )}
        </ul>
    );
};
