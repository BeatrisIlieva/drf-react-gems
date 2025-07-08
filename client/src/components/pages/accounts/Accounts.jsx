import { Outlet } from 'react-router';
import { Nav } from '../../reusable/nav/Nav';
import { navLinks } from '../../../constants/accountsNavLinksData';
import { Header } from './header/Header';

import styles from './Accounts.module.scss';
import { Logout } from './logout/Logout';
import { PaddedContainer } from '../../reusable/padded-container/PaddedContainer';

export const Accounts = () => {
    return (
        <section className={styles['accounts']}>
            <Header />
            <div className={styles['wrapper']}>
                <PaddedContainer>
                    <div className={styles['nav-wrapper']}>
                        <Nav links={navLinks} />
                        <Logout />
                    </div>
                </PaddedContainer>
                <Outlet />
            </div>
        </section>
    );
};
