import { FilterItem } from './filter-item/FilterItem';
import { normalizeData } from './utils';

import { useProductFiltersContext } from '../../../../contexts/ProductFiltersContext';

import styles from './FilterList.module.scss';

export const FilterList = () => {
    const { collections, colors, metals, stones, displayFilters } = useProductFiltersContext();

    const filters = normalizeData(metals, colors, stones, collections);

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
