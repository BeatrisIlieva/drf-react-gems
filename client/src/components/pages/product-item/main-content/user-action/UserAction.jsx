import { ComplimentaryShipping } from '../../../../reusable/complimentary-shipping/ComplimentaryShipping';
import { StyledTextBlock } from '../../../../reusable/styled-text-block/StyledTextBlock';
import { MiniBagPopup } from './mini-bag-popup/MiniBagPopup';
import { PriceDisplay } from './price-display/PriceDisplay';
import { ProductActions } from './product-actions/ProductActions';
import { RelatedProducts } from './related-products/RelatedProducts';
import { SizeList } from './size-list/SizeList';

import { useCategoryName } from '../../../../../hooks/useCategoryName';
import { usePriceCalculation } from '../../../../../hooks/usePriceCalculation';

import { useProductItemContext } from '../../../../../contexts/ProductItemContext';

import styles from './UserAction.module.scss';

export const UserAction = () => {
    const { categoryNameCapitalizedSingular } = useCategoryName();
    const {
        collectionName,
        colorName,
        stoneName,
        metalName,
        inventory,
        createShoppingBagHandler,
        notSelectedSizeError,
        isSoldOut,
        isAddingToBag,
        productId,
        toggleMiniBagPopupOpen,
        isMiniBagPopupOpen,
        selectedSize,
    } = useProductItemContext();

    const { formattedMinPrice, formattedMaxPrice, selectedInventoryItem } = usePriceCalculation(
        inventory,
        selectedSize
    );

    const sectionClassName = [
        styles['user-action'],
        isAddingToBag ? 'animate-fade-out duration-300ms' : 'animate-fade-in duration-500ms',
    ].join(' ');

    const sizeErrorClassName = [
        notSelectedSizeError ? styles['error'] : '',
        isAddingToBag ? 'animate-pulse' : '',
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
                isAddingToBag={isAddingToBag}
            />

            <RelatedProducts />

            <p className={sizeErrorClassName}>Size:</p>

            <SizeList />

            <p className={sizeMessageClassName}>Please select a size.</p>

            <ProductActions
                productId={productId}
                isSoldOut={isSoldOut}
                isAddingToBag={isAddingToBag}
                createShoppingBagHandler={createShoppingBagHandler}
            />

            <ComplimentaryShipping />

            <MiniBagPopup isOpen={isMiniBagPopupOpen} onClose={toggleMiniBagPopupOpen} />
        </section>
    );
};
