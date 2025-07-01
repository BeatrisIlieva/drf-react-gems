import { Outlet } from 'react-router';
import { Nav } from '../../reusable/nav/Nav';
import { navLinks } from '../../../constants/accountsNavLinksData';
import { Header } from './header/Header';

import styles from './Accounts.module.scss';

export const Accounts = () => {
    return (
        <section className={styles['accounts']}>
            <Header />
            <div className={styles['wrapper']}>
                <Nav links={navLinks} />
                <Outlet />
            </div>
        </section>
    );
};
