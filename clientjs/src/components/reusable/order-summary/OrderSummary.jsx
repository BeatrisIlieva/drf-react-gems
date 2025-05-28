import styles from './OrderSummary.module.css';
import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';
import { FlexTextRow } from '../flex-text-row/FlexTextRow';

import { getTextRows } from './utils';
import { Button } from '../button/Button';
import { ComplimentaryShipping } from '../complimentary-shipping/ComplimentaryShipping';

export const OrderSummary = ({ children }) => {
    const { shoppingBagTotalPrice } = useShoppingBagContext();
    const textRows = getTextRows(shoppingBagTotalPrice);

    return (
        <section className={styles['order-summary']}>
            <h3>Order Summary</h3>

            <div>
                {textRows.map((row) => (
                    <FlexTextRow {...row} />
                ))}
            </div>

            <Button
                title={'Continue Checkout'}
                color={'black'}
                actionType={'button'}
            />

            <ComplimentaryShipping />
        </section>
    );
};
