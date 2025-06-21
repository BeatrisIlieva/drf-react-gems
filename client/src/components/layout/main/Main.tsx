import type { ReactElement } from 'react';
import { Route, Routes } from 'react-router';

import { ProductListProvider } from '../../../providers/ProductListProvider';
import { ProductList } from '../../pages/product-list/ProductList';

import styles from './Main.module.scss';
import { Home } from '../../pages/home/Home';
import { ProductFiltersProvider } from '../../../providers/ProductFiltersProvider';

export const Main = (): ReactElement => {
    return (
        <main className={styles['main']}>
            <Routes>
                <Route path='/' element={<Home />} />

                <Route
                    path='/products/:categoryName'
                    element={
                        <ProductFiltersProvider>
                            <ProductListProvider>
                                <ProductList />
                            </ProductListProvider>
                        </ProductFiltersProvider>
                    }
                />
            </Routes>
        </main>
    );
};
