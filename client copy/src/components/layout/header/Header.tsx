import { useEffect, type ReactElement, useRef } from 'react';
import { Logo } from './logo/Logo';
import { Nav } from './nav/Nav';
import { Buttons } from './buttons/Buttons';
import styles from './Header.module.scss';
import { useSentinel } from '../../../hooks/useSentinel';

export const Header = (): ReactElement => {
    const headerRef = useRef<HTMLElement | null>(null);

    const { sentinelRef, isSticky } = useSentinel();

    useEffect(() => {
        let lastScrollY = 0;

        const handleScroll = () => {
            const currentScrollY = window.scrollY;
            const header = headerRef.current;
            if (!header) return;

            if (currentScrollY > 0 && currentScrollY > lastScrollY) {
                header.classList.remove(styles.visible);
                header.classList.add(styles.hidden);
            } else if (currentScrollY < lastScrollY) {
                header.classList.remove(styles.hidden);
                header.classList.add(styles.visible);
            }

            lastScrollY = currentScrollY;
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <>
            <div ref={sentinelRef} className={styles['sentinel']} />

            <header
                ref={headerRef}
                className={`${styles['header']} ${styles['visible']} ${isSticky ? styles['sticky'] : ''}`}
            >
                <Logo />
                <Nav />
                <Buttons />
            </header>
        </>
    );
};
