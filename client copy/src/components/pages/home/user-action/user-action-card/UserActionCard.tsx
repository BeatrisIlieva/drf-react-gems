import type { ReactElement } from 'react';

import styles from './UserActionCard.module.scss';

interface Props {
    category: string;
    imageUrl: string;
}

export const UserActionCard = ({ category, imageUrl }: Props): ReactElement => {
    return (
        <li className={styles['thumbnail']}>
            <h5>{category}S</h5>
            <img src={imageUrl} alt={`${category}-image`} />
        </li>
    );
};
