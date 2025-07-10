import { ShadowBox } from '../../../reusable/shadow-box/ShadowBox';
import { ShoppingBagItem } from './shopping-bag-item/ShoppingBagItem';

import { useShoppingBagContext } from '../../../../contexts/ShoppingBagContext';

import styles from './ShoppingBagList.module.scss';

export const ShoppingBagList = () => {
    const { shoppingBagItems } = useShoppingBagContext();

    return (
        <ShadowBox>
            <ul className={styles['shopping-bag-list']}>
                {shoppingBagItems.map(item => (
                    <ShoppingBagItem key={item.id} {...item} />
                ))}
            </ul>
        </ShadowBox>
    );
};
