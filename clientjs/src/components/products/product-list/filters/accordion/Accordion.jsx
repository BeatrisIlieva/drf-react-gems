import { useState } from 'react';

import styles from './Accordion.module.css';
import { ArrowUpIcon } from '../../../../reusable/arrow-up-icon/ArrowUpIcon';
import { ArrowDownIcon } from '../../../../reusable/arrow-down-icon/ArrowDownIcon';
import { SelectionBox } from './selection-box/SelectionBox';
import { ColorSelector } from './color-selector/ColorSelector';
import { MaterialSelector } from './material-selector/MaterialSelector';
import { useProductContext } from '../../../../../contexts/ProductContext';

export const Accordion = ({ data, isLast }) => {
    const {
        stonesData,
        colorsData,
        addColorToFiltration,
        removeColorFromFiltration,
        addStoneToFiltration,
        removeStoneFromFiltration
    } = useProductContext();

    const [displayFilterItem, setDisplayFilterItem] = useState(false);

    const toggleDisplayFilterItem = () => {
        setDisplayFilterItem(() => !displayFilterItem);
    };

    return (
        <div className={styles['accordion']}>
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
                        Object.entries(colorsData).map(([color, value]) => (
                            <SelectionBox
                                key={color}
                                removeHandler={removeColorFromFiltration}
                                itemId={value.id}
                            >
                                <ColorSelector
                                    key={color}
                                    title={color}
                                    count={value.count}
                                    hex={value.hex_code}
                                    itemId={value.id}
                                    addFiltration={addColorToFiltration}
                                />
                            </SelectionBox>
                        ))
                    ) : data.title === 'Stone' ? (
                        Object.entries(stonesData).map(([stone, value]) => (
                            <SelectionBox
                                key={stone}
                                removeHandler={removeStoneFromFiltration}
                                itemId={value.id}
                            >
                                <ColorSelector
                                    key={stone}
                                    title={stone}
                                    count={value.count}
                                    image={value.image}
                                    itemId={value.id}
                                    addFiltration={addStoneToFiltration}
                                />
                            </SelectionBox>
                        ))
                    ) : data.title === 'Material' ? (
                        <MaterialSelector />
                    ) : null}
                </li>
            </ul>
        </div>
    );
};
