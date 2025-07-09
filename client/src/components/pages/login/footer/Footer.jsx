import React from 'react';

import { useNavigate } from 'react-router';

import { Button } from '../../../reusable/button/Button';
import { Icon } from '../../../reusable/icon/Icon';

import styles from './Footer.module.scss';

export const Footer = () => {
    const navigate = useNavigate();

    const navigateToRegisterHandler = () => {
        navigate('/my-account/register');
    };

    return (
        <>
            <span className={styles['border']}></span>

            <footer className={styles['footer']}>
                <h3>Don't have an account?</h3>

                <Button
                    title={'Create Account'}
                    callbackHandler={navigateToRegisterHandler}
                    color={'black'}
                    actionType={'button'}
                    pending={false}
                />

                <span className={styles['border']}></span>

                <h6>What's included in your Account</h6>
                <ul>
                    <li>
                        <Icon name="bag" fontSize={1} />
                        <span>Faster checkout</span>
                    </li>
                    <li>
                        <Icon name="heart" fontSize={1} />
                        <span>Save your wish list</span>
                    </li>
                    <li>
                        <Icon name="user" fontSize={1} />
                        <span>Manage your personal information</span>
                    </li>
                </ul>
            </footer>
        </>
    );
};
