import styles from './SizeItem.module.css';

export const SizeItem = ({ size, quantity, selectedSize, clickHandler }) => {
    return (
        <li
            key={size.id}
            className={`${styles['size-item']} ${
                selectedSize === size.name ? styles['selected'] : ''
            } ${quantity < 1 ? styles['sold-out'] : ''}`.trim()}
        >
            <button disabled={quantity < 1} onClick={() => clickHandler(size.name)}>
                <span>{size.name}</span>
                <span>cm</span>
            </button>
        </li>
    );
};
