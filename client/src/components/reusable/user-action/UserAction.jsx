import { ComplimentaryShipping } from '../complimentary-shipping/ComplimentaryShipping';
import { StyledTextBlock } from '../styled-text-block/StyledTextBlock';
import { PriceDisplay } from './price-display/PriceDisplay';
import { ProductActions } from './product-actions/ProductActions';
import { RelatedProducts } from './related-products/RelatedProducts';
import { SizeList } from './size-list/SizeList';

import { useCategoryName } from '../../../hooks/useCategoryName';
import { usePriceCalculation } from '../../../hooks/usePriceCalculation';

import { useProductItemContext } from '../../../contexts/ProductItemContext';

import styles from './UserAction.module.scss';

export const UserAction = ({
    onAddToBag,
    isAddingToBag = false,
    categoryName: propCategoryName,
    hideWishlistButton = false,
}) => {
    const { categoryNameCapitalizedSingular } = useCategoryName();
    const {
        collectionName,
        colorName,
        stoneName,
        metalName,
        inventory,
        createShoppingBagHandler,
        notSelectedSizeError,
        productId,
        selectedSize,
    } = useProductItemContext();

    const { formattedMinPrice, formattedMaxPrice, selectedInventoryItem } = usePriceCalculation(
        inventory,
        selectedSize
    );

    const handleAddToBag = onAddToBag || createShoppingBagHandler;
    const isAdding = isAddingToBag || false;

    const sectionClassName = [
        styles['user-action'],
        isAdding ? 'animate-fade-out duration-300ms' : 'animate-fade-in duration-500ms',
    ].join(' ');

    const sizeErrorClassName = [
        notSelectedSizeError ? styles['error'] : '',
        isAdding ? 'animate-pulse' : '',
    ]
        .filter(Boolean)
        .join(' ');

    const sizeMessageClassName = [notSelectedSizeError ? styles['error'] : styles['invisible']]
        .filter(Boolean)
        .join(' ');

    return (
        <section className={sectionClassName}>
            <h1>
                <span>{collectionName}</span>
                <span>{categoryNameCapitalizedSingular}</span>
            </h1>

            <StyledTextBlock
                text={`${colorName} ${stoneName} set in ${metalName}`}
                isSubtle={true}
            />

            <PriceDisplay
                selectedInventoryItem={selectedInventoryItem}
                formattedMinPrice={formattedMinPrice}
                formattedMaxPrice={formattedMaxPrice}
                isAddingToBag={isAdding}
            />

            <RelatedProducts />

            <p className={sizeErrorClassName}>Size:</p>

            <SizeList />

            <p className={sizeMessageClassName}>Please select a size.</p>

            <ProductActions
                productId={productId}
                isAddingToBag={isAdding}
                createShoppingBagHandler={handleAddToBag}
                categoryName={propCategoryName}
                hideWishlistButton={hideWishlistButton}
            />

            <ComplimentaryShipping />
        </section>
    );
};
