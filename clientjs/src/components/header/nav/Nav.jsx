import { useState, useEffect } from 'react';

import { useCategories } from '../../../api/productsApi';
import { NavItem } from './nav-item/NavItem';

import styles from './Nav.module.css';

export const Nav = () => {
    const { getCategories } = useCategories();

    const [categories, setCategories] = useState([]);

    useEffect(() => {
        getCategories().then((result) => setCategories(result));
    }, [getCategories]);

    return (
        <nav className={styles['main-nav']}>
            <ul>
                {categories.map((category) => (
                    <li key={category.id}>
                        <NavItem {...category} />
                    </li>
                ))}
            </ul>
        </nav>
    );
};
