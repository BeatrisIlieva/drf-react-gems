import { useState } from 'react';

import { XMark } from '../../../../../reusable/x-mark/XMark';
import styles from './SelectionContent.module.css';

export const SelectionContent = ({ children, addHandler, removeHandler, itemId, title, count }) => {
    const [isSelected, setIsSelected] = useState(false);

    const toggleIsSelectedHandler = () => {
        if (isSelected) {
            removeHandler(itemId);
        } else {
            addHandler(itemId);
        }

        setIsSelected(() => !isSelected);
    };
    return (
        <span
            className={`${styles['selection-content']} ${
                isSelected ? styles['selected'] : ''
            }`.trim()}
        >
            <button disabled={isSelected} onClick={toggleIsSelectedHandler}>
                {children ? children : <div></div>}
                
                <span>
                    <span>{title}</span>
                    <span>({count})</span>
                </span>
            </button>
            {isSelected && (
                <button className={styles['x-mark']} onClick={toggleIsSelectedHandler}>
                    <XMark />
                </button>
            )}
        </span>
    );
};
