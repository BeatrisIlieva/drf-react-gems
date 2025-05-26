
import { UserContext } from './contexts/UserContext';
import { Register } from './components/accounts/register/Register';
import { Logout } from './components/accounts/logout/Logout';
import { Login } from './components/accounts/login/Login';
import { Delete } from './components/accounts/delete/Delete';
import { Route, Routes } from 'react-router';
import { Home } from './components/home/Home';
import { Header } from './components/header/Header';
import { Footer } from './components/footer/Footer';
import { Details } from './components/accounts/details/Details';
import styles from './App.module.css';
import { AuthGuard } from './guards/AuthGuard';
import { ScrollToTop } from './components/scroll-to-top/ScrollToTop';
import { ProductList } from './components/products/product-list/ProductList';
import { ProductProvider } from './contexts/ProductContext';
import { ProductItem } from './components/products/product-item/ProductItem';

function App() {
    // const [products, setProducts] = useState([]);

    // useEffect(() => {
    //     try {
    //         fetch(`http://localhost:8000/products?category=${1}`)
    //         .then((response) => response.json())
    //         .then((result) => setProducts(result));
    //     } catch(err) {
    //         console.log(err.message)
    //     }

    // }, []);

    return (
        <div className={styles['body']}>
            <Header />
            <main className={styles['main']}>
                <Routes>
                    <Route index element={<Home />} />
                    <Route path='/my-account/register' element={<Register />} />
                    <Route path='/my-account/login' element={<Login />} />

                    <Route
                        path='/products/:categoryName'
                        element={
                            <ProductProvider>
                                <ProductList />
                            </ProductProvider>
                        }
                    />

                    <Route
                        path='/products/:categoryName/:productId'
                        element={
                            // <ProductProvider>
                                <ProductItem />
                            // </ProductProvider>
                        }
                    />

                    <Route element={<AuthGuard />}>
                        <Route path='/my-account/details' element={<Details />} />
                    </Route>
                </Routes>
            </main>

            <Footer />
            <ScrollToTop />
        </div>
    );
}

export default App;
