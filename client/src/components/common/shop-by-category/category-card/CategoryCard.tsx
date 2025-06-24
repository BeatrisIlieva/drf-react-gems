import type { ReactElement } from 'react';

import styles from './CategoryCard.module.scss';
import { Link } from 'react-router';

interface Props {
    category: string;
    imageUrl: string;
}

export const CategoryCard = ({
    category,
    imageUrl
}: Props): ReactElement => {
    return (
        <Link to={`/products/${category.toLowerCase()}s`}>
            <li className={styles['thumbnail']}>
                <h5>{category}S</h5>
                <img src={imageUrl} alt={`${category}-image`} />
            </li>
        </Link>
    );
};
