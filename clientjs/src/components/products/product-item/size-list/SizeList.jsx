import { SizeItem } from './size-item/SizeItem';

import styles from './SizeList.module.css';

export const SizeList = ({
    sizes,
    selectedSize,
    clickHandler,
    updateSelectedInventoryHandler,
    errorOccurred
}) => {
    return (
        <div className={styles['size-list']}>
            <span className={`${errorOccurred ? styles['error'] : ''}`.trim()}>Size:</span>
            <ul>
                {sizes.map((item) => (
                    <SizeItem
                        key={item.size.id}
                        size={item.size}
                        quantity={item.quantity}
                        selectedSize={selectedSize}
                        clickHandler={clickHandler}
                        updateSelectedInventoryHandler={updateSelectedInventoryHandler}
                        contentType={item.content_type}
                        objectId={item.object_id}
                        errorOccurred={errorOccurred}
                    />
                ))}
            </ul>
            {errorOccurred && (
                <p>Please select a size</p>
            )}
        </div>
    );
};
