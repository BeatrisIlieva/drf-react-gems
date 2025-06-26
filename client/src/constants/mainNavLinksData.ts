export interface NavLink {
    title: string;
    path: string;
}

export const navLinks: NavLink[] = [
    { title: 'Earwears', path: '/products/earwears' },
    { title: 'Neckwears', path: '/products/neckwears' },
    { title: 'Wristwears', path: '/products/wristwears' },
    { title: 'Fingerwears', path: '/products/fingerwears' }
];
