import { useState } from 'react';
import styles from './SelectionBox.module.css';

import { XMark } from '../../../../../reusable/x-mark/XMark';

export const SelectionBox = ({ children }) => {
    const [isSelected, setIsSelected] = useState(false);

    const toggleIsSelectedHandler = () => {
        setIsSelected(() => !isSelected);
        console.log('click');
    };

    return (
        <span
            className={`${styles['selection-box']} ${
                isSelected ? styles['selected'] : ''
            }`.trim()}
        >
            <button disabled={isSelected} onClick={toggleIsSelectedHandler}>
                {children}
            </button>
            {isSelected && (
                <button
                    className={styles['x-mark']}
                    onClick={toggleIsSelectedHandler}
                >
                    <XMark />
                </button>
            )}
        </span>
    );
};
