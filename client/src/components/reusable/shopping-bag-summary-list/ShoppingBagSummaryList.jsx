import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';
import { Delivery } from '../delivery/Delivery';
import { OrderSummary } from '../order-summary/OrderSummary';
import { ShadowBox } from '../shadow-box/ShadowBox';
import { ShoppingBagSummaryItem } from './shopping-bag-summary-item/ShoppingBagSummaryItem';
import styles from './ShoppingBagSummaryList.module.scss';

export const ShoppingBagSummaryList = () => {
    const { shoppingBagItems, isLoading } =
        useShoppingBagContext();

    if (isLoading) {
        return (
            <ShadowBox>
                <section
                    className={
                        styles['shopping-bag-summary-list']
                    }
                >
                    <div className={styles['loading']}>
                        Loading...
                    </div>
                </section>
            </ShadowBox>
        );
    }

    if (!shoppingBagItems || shoppingBagItems.length === 0) {
        return (
            <ShadowBox>
                <section
                    className={
                        styles['shopping-bag-summary-list']
                    }
                >
                    <div className={styles['empty']}>
                        Your bag is empty
                    </div>
                </section>
            </ShadowBox>
        );
    }

    return (
        <ShadowBox>
            <section
                className={styles['shopping-bag-summary-list']}
            >
                <Delivery fontSize={1.4} />
                <ul>
                    {shoppingBagItems.map((item) => (
                        <ShoppingBagSummaryItem
                            key={item.id}
                            {...item}
                        />
                    ))}
                </ul>
            </section>
        </ShadowBox>
    );
};
