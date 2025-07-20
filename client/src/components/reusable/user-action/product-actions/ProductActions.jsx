import { Button } from '../../button/Button';
import { Icon } from '../../icon/Icon';

import { useCategoryName } from '../../../../hooks/useCategoryName';

import { useProductItemContext } from '../../../../contexts/ProductItemContext';
import { useWishlistContext } from '../../../../contexts/WishlistContext';

import styles from './ProductActions.module.scss';

export const ProductActions = ({
    productId,
    isAddingToBag,
    createShoppingBagHandler,
    categoryName: propCategoryName,
    hideWishlistButton = false,
}) => {
    const { categoryName: contextCategoryName } = useCategoryName();
    const { isInWishlist, handleWishlistToggle } = useWishlistContext();
    const { isSoldOut } = useProductItemContext();

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
                disabled={isAddingToBag || isSoldOut}
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
