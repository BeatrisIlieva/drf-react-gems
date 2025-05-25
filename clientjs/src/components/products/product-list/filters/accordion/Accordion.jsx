import { useEffect, useState } from 'react';
import { useLocation } from 'react-router';
import styles from './Accordion.module.css';
import { ArrowUpIcon } from '../../../../reusable/arrow-up-icon/ArrowUpIcon';
import { ArrowDownIcon } from '../../../../reusable/arrow-down-icon/ArrowDownIcon';
import { MaterialSelector } from './material-selector/MaterialSelector';
import { ColorSelector } from './color-selector/ColorSelector';
import { StoneSelector } from './stone-selector/StoneSelector';
import { PriceSelector } from './price-selector/PriceSelector';
import { CollectionSelector } from './collection-selector/CollectionSelector';

export const Accordion = ({ data }) => {
    const [displayFilterItem, setDisplayFilterItem] = useState(false);
    const location = useLocation();

    useEffect(() => {
        setDisplayFilterItem(false);
    }, [location]);

    const toggleDisplayFilterItem = () => {
        setDisplayFilterItem(() => !displayFilterItem);
    };

    return (
        <div>
            <div className={styles['filter-title']}>
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
                    ) : data.title === 'Price' ? (
                        <PriceSelector />
                    ) : data.title === 'Collection' ? (
                        <CollectionSelector />
                    )
                    : null}
                </li>
            </ul>
        </div>
    );
};
