import type { ReactElement } from 'react';
import { Route, Routes } from 'react-router';

import { ProductListProvider } from '../../../providers/ProductListProvider';
import { ProductList } from '../../pages/product-list/ProductList';

import styles from './Main.module.scss';

export const Main = (): ReactElement => {
    return (
        <main className={styles['main']}>
            <Routes>
                <Route
                    path='/products/:categoryName'
                    element={
                        <ProductListProvider>
                            <ProductList />
                        </ProductListProvider>
                    }
                />
            </Routes>
        </main>
    );
};
