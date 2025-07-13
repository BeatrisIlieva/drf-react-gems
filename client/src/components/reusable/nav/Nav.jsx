import { NavLink } from 'react-router';

import { usePermissions } from '../../../hooks/usePermissions';

import styles from './Nav.module.scss';

export const Nav = ({ links, flexDirection = 'row', onLinkClick = null }) => {
    const { isReviewer } = usePermissions();


    const filteredLinks = links.filter(link => {

        if (link.requiresReviewer) {
            return isReviewer();
        }

        return true;
    });

    return (
        <nav className={styles['main-nav']}>
            <ul style={{ flexDirection }}>
                {filteredLinks.map(link => (
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
