import { UserContext } from './contexts/UserContext';
import { Register } from './components/accounts/register/Register';
import { Login } from './components/accounts/login/Login';
import { Route, Routes } from 'react-router';
import { Home } from './components/home/Home';
import { Header } from './components/header/Header';
import { Footer } from './components/footer/Footer';
import { Details } from './components/accounts/details/Details';
import styles from './App.module.css';
import { AuthGuard } from './guards/AuthGuard';
import { ScrollToTop } from './components/scroll-to-top/ScrollToTop';
import { ProductList } from './components/products/product-list/ProductList';
import { ProductListProvider } from './contexts/ProductListContext';
import { ProductItem } from './components/products/product-item/ProductItem';
import { ProductItemProvider } from './contexts/ProductItemContext';
import { ShoppingBag } from './components/shopping-bag/ShoppingBag';
import { ShoppingBagProvider } from './contexts/ShoppingBagContext';

function App() {
    return (
        <div className={styles['body']}>
            {/* <ShoppingBagProvider> */}
                <Header />
            {/* </ShoppingBagProvider> */}
            <main className={styles['main']}>
                <Routes>
                    <Route index element={<Home />} />
                    <Route path='/my-account/register' element={<Register />} />
                    <Route path='/my-account/login' element={<Login />} />
                    <Route
                        path='/user/shopping-bag'
                        element={
                            <ShoppingBagProvider>
                                <ShoppingBag />
                            </ShoppingBagProvider>
                        }
                    />

                    <Route
                        path='/products/:categoryName'
                        element={
                            <ProductListProvider>
                                <ProductList />
                            </ProductListProvider>
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

                    <Route element={<AuthGuard />}>
                        <Route
                            path='/my-account/details'
                            element={<Details />}
                        />
                    </Route>
                </Routes>
            </main>

            <Footer />
            <ScrollToTop />
        </div>
    );
}

export default App;
