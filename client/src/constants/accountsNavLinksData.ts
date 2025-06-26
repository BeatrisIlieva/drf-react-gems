export interface NavLink {
    title: string;
    path: string;
}

export const navLinks: NavLink[] = [
    { title: 'Account Details', path: '/my-account/details' },
    { title: 'Order History', path: '/my-account/orders' }
];
