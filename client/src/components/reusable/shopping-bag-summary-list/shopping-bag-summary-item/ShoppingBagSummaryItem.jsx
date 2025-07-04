import { formatPrice } from '../../../../utils/formatPrice';
import { FlexTextRow } from '../../flex-text-row/FlexTextRow';
import styles from './ShoppingBagSummaryItem.module.scss';

export const ShoppingBagSummaryItem = ({
    quantity,
    totalPricePerProduct,
    productInfo
}) => {
    const formattedTotalPricePerProduct = formatPrice(
        totalPricePerProduct.toString()
    );

    return (
        <li className={styles['shopping-bag-summary-item']}>
            <span className={styles['thumbnail']}>
                <img
                    src={productInfo.firstImage}
                    alt={productInfo.collection}
                />
            </span>

            <div className={styles['wrapper']}>
                <FlexTextRow
                    firstWord={`${productInfo.collection} ${productInfo.category}`}
                    secondWord={`${formattedTotalPricePerProduct}`}
                    firstWordImportance={'highlighted'}
                    secondWordImportance={'highlighted'}
                />

                <p>
                    {`${productInfo.color} ${productInfo.stone} set in ${productInfo.metal}`}
                </p>

                <FlexTextRow
                    firstWord={`Size: ${productInfo.size}`}
                    secondWord={`Qty ${quantity}`}
                    firstWordImportance={'subtle'}
                    secondWordImportance={'subtle'}
                />
            </div>
        </li>
    );
};
