import { Icon } from '../../../../../reusable/icon/Icon';
import { Visualization } from './visualization/Visualization';

import styles from './Button.module.scss';

export const Button = ({ item, isSelected, onToggle }) => {
    return (
        <li className={`${styles['item']} ${isSelected ? styles['selected'] : ''}`}>
            <button
                disabled={isSelected}
                className={styles['add-filter']}
                onClick={() => onToggle(item.id)}
            >
                <Visualization item={item} />
                <span>{item.label}</span>
                <span className={styles['count']}>({item.count})</span>
            </button>

            {isSelected && (
                <div className={styles['remove-filter']} onClick={() => onToggle(item.id)}>
                    <Icon name="xMark" isSubtle={true} fontSize={0.7} />
                </div>
            )}
        </li>
    );
};
