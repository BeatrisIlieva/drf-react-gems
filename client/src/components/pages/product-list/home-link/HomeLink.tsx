import type { ReactElement } from 'react';
import { useCategoryName } from '../../../../hooks/useCategoryName';
import { Link } from 'react-router';

import styles from './HomeLink.module.scss';

export const HomeLink = (): ReactElement => {
    const { categoryNameCapitalizedPlural } = useCategoryName();

    return (
        <p className={styles['home-link']}>
            <Link to={'/'}>Home</Link>
            <span>/</span>
            <span>{categoryNameCapitalizedPlural}</span>
        </p>
    );
};
