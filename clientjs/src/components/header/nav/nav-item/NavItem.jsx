import { Link } from 'react-router';

import styles from './NavItem.module.css';

export const NavItem = ({ id, name }) => {
    
    return (
        <Link to={`/products/${name.toLowerCase()}/${id}`} className={styles['nav-item']}>
            <span>{name}</span>
        </Link>
    );
};
