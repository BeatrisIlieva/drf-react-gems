import { type ReactElement } from 'react';

import styles from './Nav.module.scss';
import { Icon } from '../../../reusable/icon/Icon';
import { SortBy } from './sort-by/SortBy';

export const Nav = (): ReactElement => {
    return (
        <nav className={styles['filters']}>
            <ul>
                <li>
                    <span>filters</span>
                    <Icon name={'filter'} fontSize={0.8} />
                </li>
                <SortBy />
            </ul>
        </nav>
    );
};
