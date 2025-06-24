import { Header } from './components/layout/header/Header';

import styles from './App.module.scss';
import { ScrollToTop } from './components/layout/scroll-to-top/ScrollToTop';
import { Footer } from './components/layout/footer/Footer';
import ShoppingBagProvider from './providers/ShoppingBagProvider';
import { Route, Routes } from 'react-router';
import { Home } from './components/pages/home/Home';

import { ProductFiltersProvider } from './providers/ProductFiltersProvider';
import { ProductListProvider } from './providers/ProductListProvider';
import { ProductList } from './components/pages/product-list/ProductList';
import { ProductItemProvider } from './providers/ProductItemProvider';
import { ProductItem } from './components/pages/product-item/ProductItem';
import { ShoppingBag } from './components/pages/shopping-bag/ShoppingBag';
import { Register } from './components/accounts/register/Register';
import { Login } from './components/accounts/login/Login';
import { Details } from './components/accounts/details/Details';
import { AuthGuard } from './guards/AuthGuard';



function App() {
    return (
        <div className={styles['app']}>
            <ShoppingBagProvider>
                <Header />
                <main className={styles['main']}>
                    <Routes>
                        <Route path='/' element={<Home />} />
                        <Route
                            path='/my-account/register'
                            element={<Register />}
                        />
                        <Route
                            path='/my-account/login'
                            element={<Login />}
                        />

                        <Route element={<AuthGuard />}>
                            <Route
                                path='/my-account/details'
                                element={<Details />}
                            />
                        </Route>
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
                        <Route
                            path='/products/:categoryName/:productId'
                            element={
                                <ProductItemProvider>
                                    <ProductItem />
                                </ProductItemProvider>
                            }
                        />
                        <Route
                            path='/user/shopping-bag'
                            element={<ShoppingBag />}
                        />
                    </Routes>
                </main>
            </ShoppingBagProvider>
            <ScrollToTop />
            <Footer />
        </div>
    );
}

export default App;
