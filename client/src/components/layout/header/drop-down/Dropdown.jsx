import { Nav } from '../../../reusable/nav/Nav';

import { navLinks } from '../../../../constants/mainNavLinksData';

import styles from './Dropdown.module.scss';

export const Dropdown = ({ onClose }) => {
    return (
        <div className={styles['dropdown']}>
            <Nav links={navLinks} flexDirection="column" onLinkClick={onClose} />
        </div>
    );
};
