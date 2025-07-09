import { StrictMode } from 'react';

import { BrowserRouter } from 'react-router';

import App from './App.jsx';
import './styles/site.scss';
import { createRoot } from 'react-dom/client';

createRoot(document.getElementById('root')).render(
    <StrictMode>
        <BrowserRouter>
            <App />
        </BrowserRouter>
    </StrictMode>
);
