import styles from './MaterialsInfo.module.css';

import { StoneImage } from './stone-image/StoneImage';

export const MaterialsInfo = ({ id, stones, materials_count }) => {
    return (
        <span className={styles['materials-info']}>
            <span className={styles['stones']}>
                {stones.map((item) => (
                    <StoneImage
                        key={`${id}-${item.color}-${item.stone}`}
                        {...item}
                        id={id}
                    />
                ))}
            </span>
            <span className={styles['materials']}>
                <span>{materials_count}</span>
                <span>{materials_count > 1 ? 'metals' : 'metal'}</span>
            </span>
        </span>
    );
};
