import { StrictMode } from 'react';

import { BrowserRouter } from 'react-router';

import App from './App.jsx';
import './styles/site.scss';
import { createRoot } from 'react-dom/client';

import { ShoppingBagProvider } from './providers/ShoppingBagProvider';
import { UserProvider } from './providers/UserProvider';
import { WishlistProvider } from './providers/WishlistProvider';

createRoot(document.getElementById('root')).render(
    <StrictMode>
        <BrowserRouter>
            <UserProvider>
                <WishlistProvider>
                    <ShoppingBagProvider>
                        <App />
                    </ShoppingBagProvider>
                </WishlistProvider>
            </UserProvider>
        </BrowserRouter>
    </StrictMode>
);
