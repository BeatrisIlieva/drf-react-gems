import { Icon } from '../../../../reusable/icon/Icon';

import { useProductFiltersContext } from '../../../../../contexts/ProductFiltersContext';

import styles from './Filters.module.scss';

export const Filters = () => {
    const { toggleDisplayFilters, displayFilters } = useProductFiltersContext();

    return (
        <li className={styles['filters']} onClick={toggleDisplayFilters}>
            <span>{displayFilters ? 'hide filters' : 'filters'}</span>
            <Icon name={'filter'} fontSize={0.85} />
        </li>
    );
};
