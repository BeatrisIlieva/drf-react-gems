import { SizeItem } from './size-item/SizeItem';

import { useProductItemContext } from '../../../../contexts/ProductItemContext';

import styles from './SizeList.module.scss';

export const SizeList = () => {
    const { inventory } = useProductItemContext();

    const items = Array.isArray(inventory) ? inventory : [];

    return (
        <ul className={styles['size-list']}>
            {items.map(item => (
                <SizeItem key={item.id} item={item} />
            ))}
        </ul>
    );
};
