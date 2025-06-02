import { type ReactElement } from 'react';

import { useProductListContext } from '../../../../../contexts/ProductListContext';
import { Icon } from '../../../../reusable/icon/Icon';

import styles from './Filters.module.scss';

export const Filters = (): ReactElement => {
    const { toggleDisplayFilters, displayFilters } =
        useProductListContext();

    return (
        <li
            className={styles['filters']}
            onClick={toggleDisplayFilters}
        >
            <span>{displayFilters ? 'hide filters' : 'filters'}</span>
            <Icon name={'filter'} fontSize={0.85} />
        </li>
    );
};
