import type { ReactElement } from 'react';
import styles from './Home.module.scss';
import { UserAction } from './user-action/UserAction';

export const Home = (): ReactElement => {
    return (
        <section className={styles['home']}>
            <div className={`${styles['thumbnail']} ${styles['wrapper-top']}`}>
                <div className={styles['hero-text']}>
                    <h2>Rare Jewels of the World</h2>
                    <p>
                        Featuring the finest diamonds and most precious gemstones, our
                        jewelry creations epitomize creativity, rarity and quality without
                        compromise.
                    </p>
                </div>
                <img
                    src='https://res.cloudinary.com/dpgvbozrb/image/upload/v1745847416/herolarged_pdp_lotuscluster_sf5pph.webp'
                    alt='hero-image'
                />
            </div>
            <div className={styles['wrapper-bottom']}>
                <div className={styles['thumbnail']}>
                    <img
                        src='https://res.cloudinary.com/dpgvbozrb/image/upload/v1745847416/lotuscluster_n1yucl.avif'
                        alt='hero-image'
                    />
                </div>
                <div className={styles['thumbnail']}>
                    <img
                        src='https://res.cloudinary.com/dpgvbozrb/image/upload/v1745847416/sbs_pdp_lotuscluster_mrnuph.jpg'
                        alt='hero-image'
                    />
                </div>
            </div>
            <UserAction />
        </section>
    );
};
