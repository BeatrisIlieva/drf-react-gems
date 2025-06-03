import type { ReactElement } from 'react';

import styles from './UserAction.module.scss';
import { UserActionCard } from './user-action-card/UserActionCard';

interface ImagesByCategories {
    [key: string]: string;
}

export const UserAction = (): ReactElement => {
    const imagesByCategories: ImagesByCategories = {
        Wristwear:
            'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748166/1_ak7nga.jpg',
        Earwear:
            'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748166/2_kg1ckf.jpg',
        Neckwear:
            'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748165/3_ukmmmx.avif',
        Fingerwear:
            'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748166/4_tmk4cj.avif'
    };

    return (
        <section className={styles['user-action']}>
            <h3>Shop By Category</h3>

            <ul className={styles['links']}>
                {Object.entries(imagesByCategories).map(([category, imageUrl]) => (
                    <UserActionCard
                        key={category}
                        category={category}
                        imageUrl={imageUrl}
                    />
                ))}
            </ul>
        </section>
    );
};
