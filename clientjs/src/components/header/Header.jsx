import { Banner } from './banner/Banner';
import { Buttons } from './buttons/Buttons';
import styles from './Header.module.css';
import { Logo } from './logo/Logo';
import { Nav } from './nav/Nav';

export const Header = () => {
    return (
        <header>
            <Banner />
            <div className={styles['logo-nav-wrapper']}>
                <div>
                    <Logo />
                    <Nav />
                </div>
                <Buttons />
            </div>
        </header>
    );
};
