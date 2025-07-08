import { useShoppingBagContext } from '../../../../contexts/ShoppingBagContext';
import styles from './ShoppingBagList.module.scss';
import { ShoppingBagItem } from './shopping-bag-item/ShoppingBagItem';
import { Skeleton } from './skeleton/Skeleton';
import { ShadowBox } from '../../../reusable/shadow-box/ShadowBox';

export const ShoppingBagList = () => {
    const {
        shoppingBagItems,
        loading
    } = useShoppingBagContext();

    if (loading && (!shoppingBagItems || shoppingBagItems.length === 0)) {
        return <Skeleton />;
    }

    return (
        <ShadowBox>
            <ul className={styles['shopping-bag-list']}>
                {shoppingBagItems.map((item) => (
                    <ShoppingBagItem key={item.id} {...item} />
                ))}
            </ul>
        </ShadowBox>
    );
};
