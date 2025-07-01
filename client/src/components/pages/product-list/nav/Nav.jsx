import { SortBy } from './sort-by/SortBy';
import { Filters } from './filters/Filters';

import styles from './Nav.module.scss';

export const Nav = () => {
    return (
        <nav className={styles['secondary-nav']}>
            <ul>
                <Filters />
                <SortBy />
            </ul>
        </nav>
    );
};
