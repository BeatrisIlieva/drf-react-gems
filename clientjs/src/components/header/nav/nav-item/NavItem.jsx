import { Link } from 'react-router';

import styles from './NavItem.module.css';

export const NavItem = ({ name }) => {
    
    return (
        <Link to={`/products/${name.toLowerCase()}`} className={styles['nav-item']}>
            <span>{name}</span>
        </Link>
    );
};
