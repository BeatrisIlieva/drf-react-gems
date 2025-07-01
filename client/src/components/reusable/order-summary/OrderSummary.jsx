import styles from './OrderSummary.module.scss';
import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';
import { getTextRows } from './utils';
import { FlexTextRow } from '../flex-text-row/FlexTextRow';
import { Skeleton } from './skeleton/Skeleton';
import { useMemo } from 'react';

export const OrderSummary = () => {
    const { shoppingBagTotalPrice, isLoading } =
        useShoppingBagContext();

    const textRows = useMemo(
        () => getTextRows(shoppingBagTotalPrice),
        [shoppingBagTotalPrice]
    );

    return (
        <section className={styles['order-summary']}>
            {isLoading ? (
                <Skeleton />
            ) : (
                <>
                    <h3>Order Summary</h3>

                    <div>
                        {textRows.map((row, index) => (
                            <FlexTextRow key={index} {...row} />
                        ))}
                    </div>
                </>
            )}
        </section>
    );
};
