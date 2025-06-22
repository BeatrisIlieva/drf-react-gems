import type { Props } from './types';
import styles from './SizeList.module.scss';

export const SizeList = ({ inventory}: Props) => {
    return (
        <ul className={styles['size-list']}>
            {inventory.map((item) => (
                <li
                    key={item.id}
                    // className={
                    //     product.id === productId
                    //         ? styles['selected']
                    //         : ''
                    // }
                >
                    <span>{item.size.name}</span>
                </li>
            ))}
        </ul>
    );
};
