import { useProductItemContext } from '../../../../contexts/ProductItemContext';
import { Button } from '../../../reusable/button/Button';
import { HeartIcon } from '../../../reusable/heart-icon/HeartIcon';

import styles from './UserAction.module.css';

export const UserAction = () => {
    const { addToBagHandler } = useProductItemContext();

    return (
        <div className={styles['user-action']}>
            <Button
                callbackHandler={addToBagHandler}
                title={'Add to Bag'}
                color={'black'}
                actionType={'button'}
            />
            <Button
                title={<HeartIcon />}
                color={'black'}
                actionType={'button'}
            />
        </div>
    );
};
