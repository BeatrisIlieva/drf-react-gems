import { useState, useEffect } from 'react';
import ProductItem from './ProductItem';
import useUserContext from './contexts/UserContext';
import { useRegister, useLogout } from './api/authApi';
import { useContext } from 'react';
import { UserContext } from './contexts/UserContext';
import { Register } from './components/accounts/register/Register';
import { Logout } from './components/accounts/logout/Logout';
import { Login } from './components/accounts/login/Login';
import { Delete } from './components/accounts/delete/Delete';
import { Route, Routes } from 'react-router';
import { Home } from './components/home/Home';
import { Header } from './components/header/Header';


function App() {
    const [products, setProducts] = useState([]);

    useEffect(() => {
        fetch(`http://localhost:8000/products?category=${1}`)
            .then((response) => response.json())
            .then((result) => setProducts(result));
    }, []);

    return (
        <>
            {/* <Delete />
            <Login />
            <Register />
            <Logout /> */}
            {/* <section className={styles['layout-item']}> */}
                <Header />
            {/* </section> */}
            <main>
                <Routes>
                    <Route index element={<Home />} />
                </Routes>
            </main>
        </>
    );
}

export default App;
