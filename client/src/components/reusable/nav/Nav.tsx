import type { ReactElement } from 'react';
import { NavLink } from 'react-router';
import styles from './Nav.module.scss';

interface NavLinkItem {
    title: string;
    path: string;
}

interface Props {
    links: NavLinkItem[];
}

export const Nav = ({ links }: Props): ReactElement => {
    return (
        <nav className={styles['main-nav']}>
            <ul>
                {links.map((link) => (
                    <li key={link.title}>
                        <NavLink
                            to={link.path}
                            className={({ isActive }) =>
                                isActive
                                    ? styles['active-link']
                                    : ''
                            }
                        >
                            {link.title}
                        </NavLink>
                    </li>
                ))}
            </ul>
        </nav>
    );
};
