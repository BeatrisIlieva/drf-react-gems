import type { ReactElement } from 'react';

import { FilterItem } from './filter-item/FilterItem';

import styles from './FilterList.module.scss';
import { useProductFiltersContext } from '../../../../contexts/ProductFiltersContext';
import { normalizeData } from './utils';
import type { NormalizedFilterGroup } from '../../../../types/Products';

export const FilterList = (): ReactElement => {
    const { collections, colors, metals, stones, displayFilters } =
        useProductFiltersContext();

    const filters: NormalizedFilterGroup[] = normalizeData(
        metals,
        colors,
        stones,
        collections
    );

    return (
        <ul
            className={`${styles['filter-list']} ${
                displayFilters ? styles['visible'] : styles['hidden']
            }`}
        >
            {filters.map(({ key, label, data }) => (
                <FilterItem key={key} label={label} data={data} />
            ))}
        </ul>
    );
};
