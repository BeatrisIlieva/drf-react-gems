import { useState } from 'react';

import styles from './Accordion.module.css';
import { ArrowUpIcon } from '../../../../reusable/arrow-up-icon/ArrowUpIcon';
import { ArrowDownIcon } from '../../../../reusable/arrow-down-icon/ArrowDownIcon';
import { SelectionBox } from './selection-box/SelectionBox';
import { ColorSelector } from './color-selector/ColorSelector';

export const Accordion = ({ data, isLast }) => {
    const [displayFilterItem, setDisplayFilterItem] = useState(false);

    const toggleDisplayFilterItem = () => {
        setDisplayFilterItem(() => !displayFilterItem);
    };

    return (
        <div className={styles['accordion']}>
            <div
                className={`${styles['filter-title']} ${
                    isLast ? styles['is-last'] : ''
                }`.trim()}
            >
                <h5>{data.title}</h5>
                <button onClick={toggleDisplayFilterItem}>
                    {displayFilterItem ? <ArrowUpIcon /> : <ArrowDownIcon />}
                </button>
            </div>

            <ul>
                <li
                    className={`${styles['filter-item']} ${
                        displayFilterItem ? styles['visible'] : ''
                    }`.trim()}
                >
                    {data.title === 'Color' ? (
                        Object.entries(data.elements).map(([color, value]) => (
                            <SelectionBox>
                                <ColorSelector
                                    key={color}
                                    color={color}
                                    count={value.count}
                                    hex={value.hex}
                                />
                            </SelectionBox>
                        ))
                    ) : (
                        <div>Other filter content</div>
                    )}
                </li>
            </ul>
        </div>
    );
};
