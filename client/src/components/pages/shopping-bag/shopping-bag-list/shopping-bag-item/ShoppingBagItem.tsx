import { type ReactElement } from 'react';
import styles from './ShoppingBagItem.module.scss';
import type { ShoppingBagItemResponse } from '../../../../../types/ShoppingBag';

import { useShoppingBagContext } from '../../../../../contexts/ShoppingBagContext';
import { QuantitySelector } from './quantity-selector/QuantitySelector';
import { formatPrice } from '../../../../../utils/formatPrice';

export const ShoppingBagItem = ({
    quantity,
    totalPricePerProduct,
    productInfo,
    id,
    contentType,
    objectId
}: ShoppingBagItemResponse): ReactElement => {
    const { deleteShoppingBagHandler, isDeleting } =
        useShoppingBagContext();

    const formattedTotalPricePerProduct = formatPrice(
        totalPricePerProduct.toString()
    );

    return (
        <li className={styles['shopping-bag-item']}>
            <span>
                <img
                    src={productInfo.firstImage}
                    alt={productInfo.collection}
                />
            </span>

            <span>
                <span>
                    <span>{`${productInfo.collection} ${productInfo.category}`}</span>

                    <span>
                        {`${productInfo.color} ${productInfo.stone} set in ${productInfo.metal}`}
                    </span>

                    <span>
                        <span>Size: {productInfo.size}</span>
                    </span>
                </span>

                <span>
                    <button>Move to Wish List</button>
                    <button
                        onClick={() => {
                            deleteShoppingBagHandler(id);
                        }}
                        disabled={isDeleting}
                        className={
                            isDeleting ? styles['removing'] : ''
                        }
                    >
                        {isDeleting ? 'Removing...' : 'Remove'}
                    </button>
                </span>
            </span>

            <span>
                <span>{`${formattedTotalPricePerProduct}`}</span>
                <QuantitySelector
                    quantity={quantity}
                    id={id}
                    contentType={contentType}
                    objectId={objectId}
                    availableQuantity={
                        productInfo.availableQuantity
                    }
                />
            </span>
        </li>
    );
};
