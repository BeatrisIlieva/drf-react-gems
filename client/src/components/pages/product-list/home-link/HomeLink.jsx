import { Link } from 'react-router';

import { useCategoryName } from '../../../../hooks/useCategoryName';

import styles from './HomeLink.module.scss';

export const HomeLink = () => {
    const { categoryNameCapitalizedPlural } = useCategoryName();

    return (
        <p className={styles['home-link']}>
            <Link to={'/'}>Home</Link>
            <span>/</span>
            <span>{categoryNameCapitalizedPlural}</span>
        </p>
    );
};
