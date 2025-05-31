import type { ReactElement } from 'react';

import { linkTitles } from './linkTitles';

import styles from './Nav.module.css';
import { Link } from 'react-router';

export const Nav = (): ReactElement => {
    return (
        <nav className={styles['main-nav']}>
            <ul>
                {linkTitles.map((title: string) => (
                    <li key={title}>
                        <Link to={`products/${title}`}>{title}</Link>
                    </li>
                ))}
            </ul>
        </nav>
    );
};
