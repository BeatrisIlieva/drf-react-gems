import { Link } from 'react-router';

import styles from './CategoryCard.module.scss';

export const CategoryCard = ({ category, imageUrl }) => {
    return (
        <Link to={`/products/${category.toLowerCase()}s`}>
            <li className={styles['thumbnail']}>
                <h5>{category}S</h5>
                <img src={imageUrl} alt={`${category}-image`} />
            </li>
        </Link>
    );
};
