import { useMemo } from 'react';

import { FlexTextRow } from '../flex-text-row/FlexTextRow';
import { ShadowBox } from '../shadow-box/ShadowBox';
import { getTextRows } from './utils';

import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';

import styles from './OrderSummary.module.scss';

export const OrderSummary = ({ children, order = 2, separate = false }) => {
    const { shoppingBagTotalPrice } = useShoppingBagContext();

    const textRows = useMemo(() => getTextRows(shoppingBagTotalPrice), [shoppingBagTotalPrice]);

    return (
        <section className={styles['order-summary']}>
            <ShadowBox title="Order Summary">
                <div className={styles['price-info']}>
                    {textRows.map((row, index) => (
                        <FlexTextRow key={index} {...row} />
                    ))}
                </div>
                {!separate && (
                    <div className={styles['children']} style={{ order: order }}>
                        {children}
                    </div>
                )}
            </ShadowBox>
            {separate && <ShadowBox>{children}</ShadowBox>}
        </section>
    );
};
