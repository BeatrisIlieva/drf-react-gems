import { useState, useEffect } from 'react';
import './App.css';
import ProductItem from './ProductItem';
import useUserContext from './contexts/UserContext';
import { useRegister, useLogout } from './api/authApi';
import { useContext } from 'react';
import { UserContext } from './contexts/UserContext';
import { Register } from './components/accounts/register/Register';



function App() {
    const { refresh, access } = useContext(UserContext);

    const [products, setProducts] = useState([]);

    const { logout } = useLogout();

    useEffect(() => {
        fetch(`http://localhost:8000/products?category=${1}`)
            .then((response) => response.json())
            .then((result) => setProducts(result));
    }, []);



    // const logoutHandler = async () => {
    //     const data = { refresh, access };

    //     try {
    //         await logout(data);

    //         userLogoutHandler();
    //     } catch (err) {
    //         console.log(err.message);
    //     }
    // };

    return (
        <>
        <Register/>
            {/* <button onClick={logoutHandler}>Sign out</button> */}

        </>
    );
}

export default App;
