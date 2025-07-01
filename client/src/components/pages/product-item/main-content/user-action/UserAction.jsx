import styles from './UserAction.module.scss';
import { useCategoryName } from '../../../../../hooks/products/useCategoryName';
import { StyledTextBlock } from '../../../../reusable/styled-text-block/StyledTextBlock';
import { formatPrice } from '../../../../../utils/formatPrice';
import { RelatedProducts } from './related-products/RelatedProducts';
import { SizeList } from './size-list/SizeList';
import { Button } from '../../../../reusable/button/Button';
import { Icon } from '../../../../reusable/icon/Icon';
import { useProductItemContext } from '../../../../../contexts/ProductItemContext';
import { ComplimentaryShipping } from '../../../../reusable/complimentary-shipping/ComplimentaryShipping';

export const UserAction = () => {
    const { categoryNameCapitalizedSingular } = useCategoryName();
    const {
        collectionName,
        colorName,
        stoneName,
        metalName,
        inventory,
        createShoppingBagHandler,
        addToWishlistHandler,
        notSelectedSizeError,
        addToCartError,
        isSoldOut
    } = useProductItemContext();

    const prices = inventory.map((item) =>
        parseFloat(item.price)
    );
    const formattedMinPrice = formatPrice(
        Math.min(...prices).toString()
    );
    const formattedMaxPrice = formatPrice(
        Math.max(...prices).toString()
    );

    return (
        <section className={styles['user-action']}>
            <h1>
                <span>{collectionName}</span>
                <span>{categoryNameCapitalizedSingular}</span>
            </h1>
            <StyledTextBlock
                text={`${colorName} ${stoneName} set in ${metalName}`}
                isSubtle={true}
            />
            <p>
                <span>{formattedMinPrice}</span>
                <span>-</span>
                <span>{formattedMaxPrice}</span>
            </p>
            <RelatedProducts />
            <p
                className={`${
                    notSelectedSizeError ? styles['error'] : ''
                }`.trim()}
            >
                Size:
            </p>
            <SizeList />
            <p
                className={`${
                    notSelectedSizeError
                        ? styles['error']
                        : styles['invisible']
                }`.trim()}
            >
                Please select a size.
            </p>

            {addToCartError && (
                <div className={styles['error-alert']}>
                    <p className={styles['error']}>
                        {addToCartError}
                    </p>
                </div>
            )}

            <div className={styles['buttons-wrapper']}>
                <Button
                    title={isSoldOut ? 'Sold Out' : 'Add to Bag'}
                    color={isSoldOut ? 'grey' : 'black'}
                    callbackHandler={createShoppingBagHandler}
                    actionType={'button'}
                    disabled={isSoldOut}
                />
                <Button
                    title={<Icon name={'heart'} />}
                    color={'black'}
                    actionType={'button'}
                    callbackHandler={addToWishlistHandler}
                />
            </div>
            <ComplimentaryShipping />
        </section>
    );
};
