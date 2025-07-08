import { Link } from 'react-router';
import styles from './OrderConfirmation.module.scss';
import { PaddedContainer } from '../../reusable/padded-container/PaddedContainer';
import { ShopByCategory } from '../../common/shop-by-category/ShopByCategory';

export const OrderConfirmation = () => {
    const title = 'Thank you for your purchase!';
    const firstLetter = title.charAt(0);

    const restOfText = title.slice(1);

    return (
        <>
            <PaddedContainer>
                <section className={styles['order-confirmation']}>
                    <h1 className={styles['title']}>
                        <span className={styles['letter-span']}>
                            {firstLetter}
                            <div
                                className={styles['thumbnail']}
                                data-testid='butterfly-container'
                            >
                                <img
                                    className={
                                        styles['butterfly']
                                    }
                                    src='https://res.cloudinary.com/deztgvefu/image/upload/v1723986117/forget-me-not-collection/miniImages/1042750_d9d98_vfqzme.gif'
                                    alt='butterfly'
                                />
                            </div>
                        </span>
                        <span>{restOfText}</span>
                    </h1>
                    <Link
                        to={'/my-account/orders'}
                        className={styles['link']}
                    >
                        <span className={styles['violet']}>
                            You can track your order details in
                            your Account.
                        </span>
                    </Link>
                </section>
            </PaddedContainer>
            <ShopByCategory />
        </>
    );
};
