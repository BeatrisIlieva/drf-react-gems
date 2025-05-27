import { useProductItemContext } from '../../../../contexts/ProductItemContext';
import { SizeItem } from './size-item/SizeItem';

import styles from './SizeList.module.css';

export const SizeList = () => {
    const { product, displayNotSelectedSizeErrorMessage } =
        useProductItemContext();

    return (
        <div className={styles['size-list']}>
            <span
                className={`${
                    displayNotSelectedSizeErrorMessage ? styles['error'] : ''
                }`.trim()}
            >
                Size:
            </span>
            <ul>
                {product.inventory.map((item) => (
                    <SizeItem
                        key={item.size.id}
                        size={item.size}
                        quantity={item.quantity}
                        contentType={item.content_type}
                        objectId={item.object_id}
                    />
                ))}
            </ul>
            {displayNotSelectedSizeErrorMessage && <p>Please select a size</p>}
        </div>
    );
};
