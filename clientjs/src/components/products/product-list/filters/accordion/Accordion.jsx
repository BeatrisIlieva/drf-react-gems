import { useState } from 'react';

import styles from './Accordion.module.css';
import { ArrowUpIcon } from '../../../../reusable/arrow-up-icon/ArrowUpIcon';
import { ArrowDownIcon } from '../../../../reusable/arrow-down-icon/ArrowDownIcon';
import { MaterialSelector } from './material-selector/MaterialSelector';
import { ColorSelector } from './color-selector/ColorSelector';
import { StoneSelector } from './stone-selector/StoneSelector';

export const Accordion = ({ data, isLast }) => {
    const [displayFilterItem, setDisplayFilterItem] = useState(false);

    const toggleDisplayFilterItem = () => {
        setDisplayFilterItem(() => !displayFilterItem);
    };

    return (
        <div>
            <div className={`${styles['filter-title']} ${isLast ? styles['is-last'] : ''}`.trim()}>
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
                        <ColorSelector />
                    ) : data.title === 'Stone' ? (
                        <StoneSelector />
                    ) : data.title === 'Material' ? (
                        <MaterialSelector />
                    ) : null}
                </li>
            </ul>
        </div>
    );
};
