import { useProductItemContext } from '../../../../../../contexts/ProductItemContext';
import styles from './SizeList.module.scss';

export const SizeList = () => {
    const { inventory, selectedSize, setSelectedSizeHandler } =
        useProductItemContext();

    return (
        <ul className={styles['size-list']}>
            {inventory!.map((item) => (
                <li key={item.id}>
                    <button
                        className={`${
                            item.quantity === 0
                                ? styles['sold-out']
                                : ''
                        } ${selectedSize === item.size.id ? styles['selected'] : ''}`.trim()}
                        disabled={item.quantity === 0}
                        onClick={() =>
                            setSelectedSizeHandler(item.size.id)
                        }
                    >
                        {item.size.name}
                    </button>
                </li>
            ))}
        </ul>
    );
};
