import { NavLink } from 'react-router';
import styles from './Nav.module.scss';

export const Nav = ({ links }) => {
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
