import type { ReactElement } from 'react';

import { Icon } from '../../../reusable/icon/Icon';

import styles from './Buttons.module.scss';

export const Buttons = (): ReactElement => {
    return (
        <ul className={styles['buttons']}>
            <li>
                <Icon name={'search'} width={0.7} />
                <span>Search</span>
            </li>

            <li>
                <Icon name={'user'} width={1} />
                <span>1</span>
            </li>

            <li>
                <Icon name={'heart'} />
                <span>8</span>
            </li>

            <li>
                <Icon name={'bag'} />
                <span>18</span>
            </li>
        </ul>
    );
};
