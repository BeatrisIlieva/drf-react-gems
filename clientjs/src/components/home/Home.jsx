import styles from './Home.module.css';
import { UserActionCard } from './user-action-card/UserActionCard';

const imagesByCategories = {
    Wristwear:
        'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748166/1_ak7nga.jpg',
    Earwear:
        'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748166/2_kg1ckf.jpg',
    Neckwear:
        'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748165/3_ukmmmx.avif',
    Fingerwear:
        'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748166/4_tmk4cj.avif'
};

export const Home = () => {
    return (
        <section className={styles['home']}>
            <div className={`${styles['thumbnail']} ${styles['wrapper-top']}`}>
                <div className={styles['hero-text']}>
                    <h2>Rare Jewels of the World</h2>
                    <p>
                        Featuring the finest diamonds and most precious
                        gemstones, our jewelry creations
                        epitomize creativity, rarity and quality without
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
            <section className={styles['user-action']}>
                <h3>Shop By Category</h3>
                <ul className={styles['links']}>
                    {Object.entries(imagesByCategories).map(
                        ([category, imageUrl]) => (
                            <li key={category} className={styles['thumbnail']}>
                                <UserActionCard
                                    category={category}
                                    imageUrl={imageUrl}
                                />
                            </li>
                        )
                    )}
                </ul>
            </section>
        </section>
    );
};
