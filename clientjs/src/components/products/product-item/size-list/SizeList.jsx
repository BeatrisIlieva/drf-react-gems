import { SizeItem } from './size-item/SizeItem';

export const SizeList = ({ sizes, selectedSize, clickHandler }) => {
    return (
        <>
            <span>Size:</span>
            <ul>
                {sizes.map((item) => (
                    <SizeItem
                        key={item.size.id}
                        size={item.size}
                        quantity={item.quantity}
                        selectedSize={selectedSize}
                        clickHandler={clickHandler}
                    />
                ))}
            </ul>
        </>
    );
};
