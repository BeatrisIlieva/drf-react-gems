import { useProductItemContext } from '../../../../../contexts/ProductItemContext';
import styles from './SizeItem.module.css';

export const SizeItem = ({ size, quantity, contentType, objectId }) => {
    const {
        selectedSize,
        updateSelectedInventoryHandler,
        displayNotSelectedSizeErrorMessage,
        selectSizeClickHandler
    } = useProductItemContext();

    const selectSizeHandler = () => {
        selectSizeClickHandler(size.name);
        updateSelectedInventoryHandler(contentType, objectId);
    };

    return (
        <li
            key={size.id}
            className={`${styles['size-item']} ${
                selectedSize === size.name ? styles['selected'] : ''
            } ${displayNotSelectedSizeErrorMessage ? styles['error'] : ''} ${
                quantity < 1 ? styles['sold-out'] : ''
            }`.trim()}
        >
            <button disabled={quantity < 1} onClick={selectSizeHandler}>
                <span>{size.name}</span>
                <span>cm</span>
            </button>
        </li>
    );
};
