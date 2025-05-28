import styles from './ShoppingBagItem.module.css';

export const ShoppingBagItem = ({
    quantity,
    content_type,
    object_id,
    total_price_per_product,
    product_info
}) => {
    const productCategory = content_type.split('inventory')[0];
    const productCategoryCapitalized =
        productCategory.charAt(0).toUpperCase() + productCategory.slice(1);
        
    return (
        <li className={styles['shopping-bag-item']}>
            <span>
                <img
                    src={product_info.first_image}
                    alt={product_info.collection}
                />
            </span>

            <span>
                <span>
                    <span>
                        {`${product_info.collection} ${product_info.reference} ${productCategoryCapitalized}`}
                    </span>

                    <span>
                        {`${product_info.color} ${product_info.stone} set in ${product_info.material}`}
                    </span>
                    {product_info.size && (
                        <span>
                            <span>{product_info.size}</span>
                            <span>cm</span>
                        </span>
                    )}
                </span>

                <span>
                    <button>Move to Wish List</button>
                    <button>Remove</button>
                </span>
            </span>

            <span>
                <span>{`$${total_price_per_product}`}</span>
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
