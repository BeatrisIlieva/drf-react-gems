import { Button } from '../../../../../reusable/button/Button';
import { Icon } from '../../../../../reusable/icon/Icon';

import { useCategoryName } from '../../../../../../hooks/useCategoryName';

import { useWishlistContext } from '../../../../../../contexts/WishlistContext';

import styles from './ProductActions.module.scss';

export const ProductActions = ({
    productId,
    isSoldOut,
    isAddingToBag,
    createShoppingBagHandler,
    categoryName: propCategoryName,
    hideWishlistButton = false, // New prop to hide wishlist button
}) => {
    const { categoryName: contextCategoryName } = useCategoryName();
    const { isInWishlist, handleWishlistToggle } = useWishlistContext();

    const categoryName = propCategoryName || contextCategoryName;
    const category = categoryName?.slice(0, categoryName?.length - 1);
    const isItemInWishlist = isInWishlist(category, productId);

    const getAddToBagTitle = () => {
        if (isAddingToBag) return 'Adding...';
        if (isSoldOut) return 'Sold Out';
        return 'Add to Bag';
    };

    const getAddToBagColor = () => {
        return isSoldOut ? 'grey' : 'black';
    };

    return (
        <div className={styles['buttons-wrapper']}>
            <Button
                title={getAddToBagTitle()}
                color={getAddToBagColor()}
                callbackHandler={createShoppingBagHandler}
                actionType="button"
                disabled={isSoldOut || isAddingToBag}
                buttonGrow="1"
                className={isAddingToBag ? 'animate-pulse' : ''}
            />
            {!hideWishlistButton && (
                <Button
                    title={<Icon name={isItemInWishlist ? 'heart-filled' : 'heart'} />}
                    color="black"
                    actionType="button"
                    callbackHandler={() => handleWishlistToggle(category + 's', productId)}
                />
            )}
        </div>
    );
};
