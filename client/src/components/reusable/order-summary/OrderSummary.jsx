import styles from './OrderSummary.module.scss';
import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';
import { getTextRows } from './utils';
import { FlexTextRow } from '../flex-text-row/FlexTextRow';
import { useMemo } from 'react';
import { ShadowBox } from '../shadow-box/ShadowBox';

export const OrderSummary = ({
    children,
    order = 2,
    separate = false
}) => {
    const { shoppingBagTotalPrice } = useShoppingBagContext();

    const textRows = useMemo(
        () => getTextRows(shoppingBagTotalPrice),
        [shoppingBagTotalPrice]
    );

    return (
        <section className={styles['order-summary']}>
            <ShadowBox title='Order Summary'>
                <div className={styles['price-info']}>
                    {textRows.map((row, index) => (
                        <FlexTextRow key={index} {...row} />
                    ))}
                </div>
                {!separate && (
                    <div
                        className={styles['children']}
                        style={{ order: order }}
                    >
                        {children}
                    </div>
                )}
            </ShadowBox>
            {separate && <ShadowBox>{children}</ShadowBox>}
        </section>
    );
};
