import { useEffect, useRef } from 'react';

import { Nav } from '../../../reusable/nav/Nav';

import { navLinks } from '../../../../constants/mainNavLinksData';

import styles from './Dropdown.module.scss';

export const Dropdown = ({ onClose }) => {
    const dropdownRef = useRef(null);

    useEffect(() => {
        const handleClick = e => {
            if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
                onClose();
            }
        };
        document.addEventListener('mousedown', handleClick);
        return () => document.removeEventListener('mousedown', handleClick);
    }, [onClose]);

    return (
        <div ref={dropdownRef} className={styles['dropdown']}>
            <Nav links={navLinks} flexDirection="column" onLinkClick={onClose} />
        </div>
    );
};
