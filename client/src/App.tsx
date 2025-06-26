import { Header } from './components/layout/header/Header';

import styles from './App.module.scss';
import { ScrollToTop } from './components/layout/scroll-to-top/ScrollToTop';
import { Footer } from './components/layout/footer/Footer';
import ShoppingBagProvider from './providers/ShoppingBagProvider';
import WishlistProvider from './providers/WishlistProvider';
import { Route, Routes, Navigate } from 'react-router';
import { Home } from './components/pages/home/Home';

import { ProductFiltersProvider } from './providers/ProductFiltersProvider';
import { ProductListProvider } from './providers/ProductListProvider';
import { ProductItemProvider } from './providers/ProductItemProvider';
import { ProductList } from './components/pages/product-list/ProductList';
import { ProductItem } from './components/pages/product-item/ProductItem';
import { ShoppingBag } from './components/pages/shopping-bag/ShoppingBag';
import { Register } from './components/pages/register/Register';
import { Login } from './components/pages/login/Login';
import { Details } from './components/pages/accounts/details/Details';
import { Orders } from './components/pages/accounts/orders/Orders';
import { AuthGuard } from './guards/AuthGuard';
import { Accounts } from './components/pages/accounts/Accounts';
import UserProvider from './providers/UserProvider';

function App() {
    return (
        <div className={styles['app']}>
            <UserProvider>
                <WishlistProvider>
                    <ShoppingBagProvider>
                        <Header />
                        <main className={styles['main']}>
                            <Routes>
                                <Route
                                    path='/'
                                    element={<Home />}
                                />
                                <Route
                                    path='/my-account/register'
                                    element={<Register />}
                                />
                                <Route
                                    path='/my-account/login'
                                    element={<Login />}
                                />
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
                                <Route element={<AuthGuard />}>
                                    <Route
                                        path='/my-account'
                                        element={<Accounts />}
                                    >
                                        <Route
                                            index
                                            element={
                                                <Navigate
                                                    to='details'
                                                    replace
                                                />
                                            }
                                        />
                                        <Route
                                            path='details'
                                            element={<Details />}
                                        />
                                        <Route
                                            path='orders'
                                            element={<Orders />}
                                        />
                                    </Route>
                                </Route>
                            </Routes>
                        </main>
                    </ShoppingBagProvider>
                    <ScrollToTop />
                    <Footer />
                </WishlistProvider>
            </UserProvider>
        </div>
    );
}

export default App;
