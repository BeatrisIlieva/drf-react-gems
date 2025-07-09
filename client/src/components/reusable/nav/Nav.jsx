import { NavLink } from 'react-router';

import styles from './Nav.module.scss';

export const Nav = ({ links, flexDirection = 'row', onLinkClick = null }) => {
    return (
        <nav className={styles['main-nav']}>
            <ul style={{ flexDirection }}>
                {links.map(link => (
                    <li key={link.title}>
                        <NavLink
                            to={link.path}
                            className={({ isActive }) => (isActive ? styles['active-link'] : '')}
                            onClick={onLinkClick}
                        >
                            {link.title}
                        </NavLink>
                    </li>
                ))}
            </ul>
        </nav>
    );
};
