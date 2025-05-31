import type { ReactElement } from 'react';

import { Logo } from './logo/Logo';
import { Nav } from './nav/Nav';
import { Buttons } from './buttons/Buttons';

import styles from './Header.module.scss';

export const Header = (): ReactElement => {
    return (
        <header className={styles['header']}>
            <Logo />
            <Nav />
            <Buttons />
        </header>
    );
};
