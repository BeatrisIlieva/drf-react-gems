import { Outlet } from 'react-router';

import { Nav } from '../../reusable/nav/Nav';
import { PaddedContainer } from '../../reusable/padded-container/PaddedContainer';
import { Header } from './header/Header';
import { Logout } from './logout/Logout';

import { navLinks } from '../../../constants/accountsNavLinksData';

import styles from './Accounts.module.scss';

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
