// import type { ReactElement } from 'react';

// import { Logo } from './logo/Logo';
// import { Nav } from './nav/Nav';
// import { Buttons } from './buttons/Buttons';

// import styles from './Header.module.scss';

// export const Header = (): ReactElement => {
//     let lastScrollY = 0;

//     window.addEventListener('scroll', (e: Event): void => {

//         const currentScrollY: number = window.scrollY;
//         const headerElement = document.querySelector('.header') as HTMLElement | null;
//         console.log(headerElement)
//         if (!headerElement) return;

//         if (currentScrollY > 100 && currentScrollY > lastScrollY) {
//             headerElement.classList.remove('visible');
//             headerElement.classList.add('hidden');
//         } else if (currentScrollY < lastScrollY) {
//             headerElement.classList.remove('hidden');
//             headerElement.classList.add('visible');
//         }

//         lastScrollY = currentScrollY;
//     });

//     return (
//         <header className={styles['header']}>
//             <Logo />
//             <Nav />
//             <Buttons />
//         </header>
//     );
// };

import { useEffect, type ReactElement, useRef } from 'react';
import { Logo } from './logo/Logo';
import { Nav } from './nav/Nav';
import { Buttons } from './buttons/Buttons';
import styles from './Header.module.scss';

export const Header = (): ReactElement => {
    const headerRef = useRef<HTMLElement | null>(null);

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
        <header ref={headerRef} className={`${styles['header']} ${styles['visible']}`}>
            <Logo />
            <Nav />
            <Buttons />
        </header>
    );
};
