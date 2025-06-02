import { type ReactElement } from 'react';

import { SortBy } from './sort-by/SortBy';
import { Filters } from './filters/Filters';

import styles from './Nav.module.scss';

export const Nav = (): ReactElement => {
    return (
        <nav className={styles['secondary-nav']}>
            <ul>
                <Filters />
                <SortBy />
            </ul>
        </nav>
    );
};
