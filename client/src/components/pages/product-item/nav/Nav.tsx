import type { ReactElement } from 'react';
import { Link } from 'react-router';
import { useCategoryName } from '../../../../hooks/products/useCategoryName';

import styles from './Nav.module.scss';

export const Nav = (): ReactElement => {
    const { categoryName, categoryNameCapitalizedPlural } =
        useCategoryName();
        
    return (
        <nav className={styles['nav']}>
            <ul>
                <li>
                    <Link to='/'>Home</Link>
                </li>
                <li>/</li>
                <li>
                    <Link to={`/products/${categoryName}`}>
                        {categoryNameCapitalizedPlural}
                    </Link>
                </li>
            </ul>
        </nav>
    );
};
