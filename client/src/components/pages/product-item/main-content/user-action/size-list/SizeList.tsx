import { useProductItemContext } from '../../../../../../contexts/ProductItemContext';
import styles from './SizeList.module.scss';

export const SizeList = () => {
    const { inventory } = useProductItemContext();
    
    return (
        <ul className={styles['size-list']}>
            {inventory!.map((item) => (
                <li
                    key={item.id}
                    className={
                        item.quantity === 0
                            ? styles['sold-out']
                            : ''
                    }
                >
                    <span>{item.size.name}</span>
                </li>
            ))}
        </ul>
    );
};
