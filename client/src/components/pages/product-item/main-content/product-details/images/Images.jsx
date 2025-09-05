import { useProductItemContext } from '../../../../../../contexts/ProductItemContext';

import styles from './Images.module.scss';

export const Images = () => {
    const { firstImage, secondImage, thirdImage, fourthImage } = useProductItemContext();

    return (
        <section className={styles['images']}>
            <div className={styles['thumbnail']}>
                <img src={thirdImage} alt="Product First Image" />
            </div>

            <div className={styles['thumbnail']}>
                <img src={fourthImage} alt="Product Second Image" />
            </div>
        </section>
    );
};
