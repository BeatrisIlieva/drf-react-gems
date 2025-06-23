import React from 'react';
import styles from './ShoppingBagItem.module.scss';

export interface ProductInfo {
    firstImage: string;
    collection: string;
    color: string;
    stone: string;
    metal: string;
    size: string;
    category: string;
}

export interface ShoppingBagItemProps {
    id: number;
    quantity: number;
    contentType: string;
    objectId: number | string;
    totalPricePerProduct: number;
    productInfo: ProductInfo;
}

export const ShoppingBagItem: React.FC<ShoppingBagItemProps> = (
    props
) => {
    const { quantity, totalPricePerProduct, productInfo } = props;

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
                        <svg
                            xmlns='http://www.w3.org/2000/svg'
                            fill='none'
                            viewBox='0 0 24 24'
                            strokeWidth={1.5}
                            stroke='currentColor'
                        >
                            <path
                                strokeLinecap='round'
                                strokeLinejoin='round'
                                d='M5 12h14'
                            />
                        </svg>
                    </button>
                    <span>{quantity}</span>
                    <button>
                        <svg
                            xmlns='http://www.w3.org/2000/svg'
                            fill='none'
                            viewBox='0 0 24 24'
                            strokeWidth={1.5}
                            stroke='currentColor'
                        >
                            <path
                                strokeLinecap='round'
                                strokeLinejoin='round'
                                d='M12 4.5v15m7.5-7.5h-15'
                            />
                        </svg>
                    </button>
                </span>
            </span>
        </li>
    );
};
