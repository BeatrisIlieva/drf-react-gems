import { Navigate, Route, Routes } from 'react-router';

import { AdminGuard } from './guards/AdminGuard';
import { AuthGuard } from './guards/AuthGuard';

import { ProductFiltersProvider } from './providers/ProductFiltersProvider';
import { ProductItemProvider } from './providers/ProductItemProvider';
import { ProductListProvider } from './providers/ProductListProvider';

import { useShoppingBagContext } from './contexts/ShoppingBagContext';

import { Footer } from './components/layout/footer/Footer';
import { Header } from './components/layout/header/Header';
import { ScrollToTop } from './components/layout/scroll-to-top/ScrollToTop';
import { Page404 } from './components/pages/Page404/Page404';
import { Accounts } from './components/pages/accounts/Accounts';
import { Details } from './components/pages/accounts/details/Details';
import { OrderHistory } from './components/pages/accounts/order-history/OrderHistory';
import { AdminPage } from './components/pages/admin/Admin';
import { Checkout } from './components/pages/checkout/Checkout';
import { Home } from './components/pages/home/Home';
import { Login } from './components/pages/login/Login';
import { OrderConfirmation } from './components/pages/order-confirmation/OrderConfirmation';
import { Payment } from './components/pages/payment/Payment';
import { ProductItem } from './components/pages/product-item/ProductItem';
import { ProductList } from './components/pages/product-list/ProductList';
import { Register } from './components/pages/register/Register';
import { ShoppingBag } from './components/pages/shopping-bag/ShoppingBag';
import { Wishlist } from './components/pages/wishlist/Wishlist';
import { MiniBagPopup } from './components/reusable/user-action/mini-bag-popup/MiniBagPopup';

import styles from './App.module.scss';

function App() {
    const { isMiniBagPopupOpen, toggleMiniBagPopupOpen } = useShoppingBagContext();

    return (
        <div className={styles['app']}>
            <Header />
            <main className={styles['main']}>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/my-account/register" element={<Register />} />
                    <Route path="/my-account/login" element={<Login />} />
                    <Route
                        path="/products/:categoryName"
                        element={
                            <ProductFiltersProvider>
                                <ProductListProvider>
                                    <ProductList />
                                </ProductListProvider>
                            </ProductFiltersProvider>
                        }
                    />
                    <Route
                        path="/products/:categoryName/:productId"
                        element={
                            <ProductItemProvider>
                                <ProductItem />
                            </ProductItemProvider>
                        }
                    />
                    <Route path="/user/shopping-bag" element={<ShoppingBag />} />
                    <Route path="/user/wishlist" element={<Wishlist />} />
                    <Route element={<AuthGuard />}>
                        <Route element={<AdminGuard />}>
                            <Route path="/admin-page" element={<AdminPage />} />
                        </Route>
                        <Route path="/my-account" element={<Accounts />}>
                            <Route index element={<Navigate to="details" replace />} />
                            <Route path="details" element={<Details />} />
                            <Route path="orders" element={<OrderHistory />} />
                        </Route>
                        <Route path="/user/checkout" element={<Checkout />} />
                        <Route path="/user/payment" element={<Payment />} />
                        <Route path="/user/order-confirmation" element={<OrderConfirmation />} />
                    </Route>
                    <Route path="*" element={<Page404 />} />
                </Routes>
            </main>
            <MiniBagPopup isOpen={isMiniBagPopupOpen} onClose={toggleMiniBagPopupOpen} />
            <ScrollToTop />
            <Footer />
        </div>
    );
}

export default App;
