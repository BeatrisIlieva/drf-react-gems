import styles from './ShoppingBagItem.module.scss';

import { useShoppingBagContext } from '../../../../../contexts/ShoppingBagContext';
import { QuantitySelector } from './quantity-selector/QuantitySelector';
import { formatPrice } from '../../../../../utils/formatPrice';

export const ShoppingBagItem = ({
    quantity,
    totalPrice,
    productInfo,
    id,
    contentType,
    objectId
}) => {
    const { deleteShoppingBagHandler, isDeleting } =
        useShoppingBagContext();

    const formattedTotalPricePerProduct = formatPrice(
        totalPrice.toString()
    );

    return (
        <li className={styles['shopping-bag-item']}>
            <span className={styles['thumbnail']}>
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
