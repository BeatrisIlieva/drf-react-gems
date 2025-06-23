import { type ReactElement } from 'react';
import styles from './ShoppingBagItem.module.scss';
import { Icon } from '../../../../reusable/icon/Icon';
import type { ProductInfo } from '../../../../../types/ShoppingBag';

interface Props {
    quantity: number;
    totalPricePerProduct: number;
    productInfo: ProductInfo;
}

export const ShoppingBagItem = ({
    quantity,
    totalPricePerProduct,
    productInfo
}: Props): ReactElement => {
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
                    <button>Remove</button>
                </span>
            </span>

            <span>
                <span>{`$${totalPricePerProduct}`}</span>
                <span>
                    <button>
                        <Icon name='minus' />
                    </button>
                    <span>{quantity}</span>
                    <button>
                        <Icon name='plus' />
                    </button>
                </span>
            </span>
        </li>
    );
};
