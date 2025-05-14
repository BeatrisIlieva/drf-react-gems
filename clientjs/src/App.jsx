import { useState, useEffect } from 'react';
import './App.css';
import ProductItem from './ProductItem';
import useUserContext from './contexts/UserContext';
import { useRegister, useLogout } from './api/authApi';
import { useContext } from 'react';
import { UserContext } from './contexts/UserContext';
import { Register } from './components/accounts/register/Register';
import { Logout } from './components/accounts/logout/Logout';
import { Login } from './components/accounts/login/Login';
import { Delete } from './components/accounts/delete/Delete';

function App() {
    const [products, setProducts] = useState([]);

    useEffect(() => {
        fetch(`http://localhost:8000/products?category=${1}`)
            .then((response) => response.json())
            .then((result) => setProducts(result));
    }, []);

    return (
        <>
            <Delete />
            <Login />
            <Register />
            <Logout />
        </>
    );
}

export default App;
