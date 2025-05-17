import { Button } from '../../../reusable/button/Button';
import styles from './Footer.module.css';

import { useNavigate } from 'react-router';

export const Footer = () => {
    const navigate = useNavigate();

    const navigateToRegisterHandler = () => {
        navigate('/my-account/register');
    };
    
    return (
        <>
            <span className={styles['border']}></span>

            <footer className={styles['footer']}>
                <h3>Don’t have an account?</h3>

                <Button
                    title={'Create Account'}
                    callbackHandler={navigateToRegisterHandler}
                    color={'black'}
                    actionType={'button'}
                    pending={false}
                />

                <span className={styles['border']}></span>

                <h6>What’s included in your Account</h6>
                <ul>
                    <li>
                        <svg
                            xmlns='http://www.w3.org/2000/svg'
                            fill='none'
                            viewBox='0 0 24 24'
                            strokeWidth={1.3}
                            stroke='black'
                        >
                            <path
                                strokeLinecap='round'
                                strokeLinejoin='round'
                                d='M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 0 1-1.12-1.243l1.264-12A1.125 1.125 0 0 1 5.513 7.5h12.974c.576 0 1.059.435 1.119 1.007ZM8.625 10.5a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm7.5 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z'
                            />
                        </svg>
                        <span>Faster checkout</span>
                    </li>
                    <li>
                        <svg
                            xmlns='http://www.w3.org/2000/svg'
                            fill='none'
                            viewBox='0 0 24 24'
                            strokeWidth={1.5}
                            stroke='currentColor'
                        >
                            <path
                                strokeLinecap='round'
                                strokeLinejoin='round'
                                d='M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z'
                            />
                        </svg>
                        <span>Save your wish list</span>
                    </li>
                    <li>
                        <svg
                            xmlns='http://www.w3.org/2000/svg'
                            fill='none'
                            viewBox='0 0 24 24'
                            strokeWidth={1.5}
                            stroke='currentColor'
                        >
                            <path
                                strokeLinecap='round'
                                strokeLinejoin='round'
                                d='M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z'
                            />
                        </svg>
                        <span>Manage personal information</span>
                    </li>
                </ul>
            </footer>
        </>
    );
};
