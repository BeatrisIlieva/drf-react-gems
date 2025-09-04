import { ShopByCategory } from '../../common/shop-by-category/ShopByCategory';

import styles from './Home.module.scss';

export const Home = () => {
    return (
        <section className={styles['home']}>
            <div className={`${styles['thumbnail']} ${styles['wrapper-top']}`}>
                <div className={styles['hero-text']}>
                    <h2>Rare Jewels of the World</h2>
                    <p>
                        Featuring the finest diamonds and most precious gemstones, our jewelry
                        creations epitomize creativity, rarity and quality without compromise.
                    </p>
                </div>
                <img
                    src="https://res.cloudinary.com/dpgvbozrb/image/upload/v1745847416/herolarged_pdp_lotuscluster_sf5pph.webp"
                    alt="hero-image"
                />
            </div>
            <div className={styles['wrapper-bottom']}>
                <div className={styles['thumbnail']}>
                    <img
                        src="https://res.cloudinary.com/dpgvbozrb/image/upload/v1745847416/lotuscluster_n1yucl.avif"
                        alt="hero-image"
                    />
                </div>
                <div className={styles['thumbnail']}>
                    <img
                        src="https://res.cloudinary.com/dpgvbozrb/image/upload/v1756919186/featuredd_midnightdatemoonphaseautomatic42mm_kuzd55.png"
                        alt="hero-image"
                    />
                </div>
                <div className={styles['thumbnail']}>
                    <img
                        src="https://res.cloudinary.com/dpgvbozrb/image/upload/v1756919187/emerald_33mm-18k_rose_gold-quartz-emeqhd33rr002-fifty_b_hfe5d1.jpg"
                        alt="hero-image"
                    />
                </div>
                <div className={styles['thumbnail']}>
                    <img
                        src="https://res.cloudinary.com/dpgvbozrb/image/upload/v1745847416/sbs_pdp_lotuscluster_mrnuph.jpg"
                        alt="hero-image"
                    />
                </div>
            </div>
            <ShopByCategory />
        </section>
    );
};
