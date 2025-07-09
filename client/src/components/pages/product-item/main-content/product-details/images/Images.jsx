import { useProductItemContext } from '../../../../../../contexts/ProductItemContext';

import styles from './Images.module.scss';

export const Images = () => {
    const { firstImage, secondImage } = useProductItemContext();

    return (
        <section className={styles['images']}>
            <div className={styles['thumbnail']}>
                <img src={firstImage} alt="Product First Image" />
            </div>

            <div className={styles['thumbnail']}>
                <img src={secondImage} alt="Product Second Image" />
            </div>
        </section>
    );
};
