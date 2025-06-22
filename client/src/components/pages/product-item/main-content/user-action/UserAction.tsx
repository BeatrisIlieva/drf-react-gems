import type { ReactElement } from 'react';
import type { Params } from './types';

import styles from './UserAction.module.scss';
import { useCategoryName } from '../../../../../hooks/products/useCategoryName';
import { StyledTextBlock } from '../../../../reusable/styled-text-block/StyledTextBlock';
import { Link } from 'react-router';
import { formatPrice } from '../../../../../utils/formatPrice';
import { RelatedProducts } from './related-products/RelatedProducts';
import { SizeList } from './size-list/SizeList';
import { Button } from '../../../../reusable/button/Button';
import { Icon } from '../../../../reusable/icon/Icon';

export const UserAction = ({
    productId,
    collectionName,
    colorName,
    stoneName,
    metalName,
    inventory,
    relatedProducts,
    firstImage
}: Params): ReactElement => {
    const { categoryNameCapitalizedSingular } = useCategoryName();

    const prices = inventory.map((item) =>
        parseFloat(item.price)
    );
    const formattedMinPrice = formatPrice(
        Math.min(...prices).toString()
    );
    const formattedMaxPrice = formatPrice(
        Math.max(...prices).toString()
    );

    const addToBagHandler = () => {};

    const addToWishlistHandler = () => {}

    return (
        <section className={styles['user-action']}>
            <h1>
                <span>{collectionName}</span>
                <span>{categoryNameCapitalizedSingular}</span>
            </h1>
            <StyledTextBlock
                text={`${colorName} ${stoneName} set in ${metalName}`}
                isSubtle={true}
            />
            <p>
                <span>{formattedMinPrice}</span>
                <span>-</span>
                <span>{formattedMaxPrice}</span>
            </p>
            <RelatedProducts
                relatedProducts={relatedProducts}
                collectionName={collectionName}
                productId={productId}
            />
            <p>Size:</p>
            <SizeList inventory={inventory} />
            <div className={styles['buttons-wrapper']}>
                <Button
                    title={'Add to Bag'}
                    color={'black'}
                    callbackHandler={addToBagHandler}
                    actionType={'button'}
                />
                <Button
                    title={<Icon name={'heart'} />}
                    color={'black'}
                    actionType={'button'}
                    callbackHandler={addToWishlistHandler}
                />
            </div>
        </section>
    );
};
