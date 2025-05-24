import { NavItem } from './nav-item/NavItem';

import styles from './Nav.module.css';

export const Nav = () => {
    const categories = ['Wristwear', 'Earwear', 'Neckwear', 'Fingerwear'];

    return (
        <nav className={styles['main-nav']}>
            <ul>
                {categories.map((category) => (
                    <li key={category}>
                        <NavItem name={category} />
                    </li>
                ))}
            </ul>
        </nav>
    );
};
