import { useProductItemContext } from '../../../../contexts/ProductItemContext';

import styles from './ProductImages.module.scss';

export const ProductImages = () => {
    const { firstImage, secondImage, thirdImage, fourthImage } = useProductItemContext();

    return (
        <section className={styles['product-images']}>
            <div>
                <img src={firstImage} alt="Product First Image" />
            </div>
            <div>
                <img src={secondImage} alt="Product Second Image" />
            </div>
            <div>
                <img src={thirdImage} alt="Product Third Image" />
            </div>
            <div>
                <img src={fourthImage} alt="Product Fourth Image" />
            </div>
        </section>
    );
};
