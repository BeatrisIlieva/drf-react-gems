import type { ReactElement } from 'react';

import { useProductListContext } from '../../../../contexts/ProductListContext';
import type { NormalizedFilterGroup } from '../../../../types/NormalizedFilter';
import { FilterItem } from './filter-item/FilterItem';
import { normalizeData } from './utils';
import styles from './FilterList.module.scss';

export const FilterList = (): ReactElement => {
    const { collections, colors, metals, prices, stones } =
        useProductListContext();

    const filters: NormalizedFilterGroup[] = normalizeData(
        metals,
        prices,
        colors,
        stones,
        collections
    );

    return (
        <ul className={styles['filter-list']}>
            {filters.map(({ key, label, data }) => (
                <FilterItem key={key} label={label} data={data} />
            ))}
        </ul>
    );
};
