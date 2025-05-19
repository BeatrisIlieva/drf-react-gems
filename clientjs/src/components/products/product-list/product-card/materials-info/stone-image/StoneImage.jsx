import { useState } from 'react';
import styles from './StoneImage.module.css';

export const StoneImage = ({ color, stone, image, product_id, id }) => {
    const [displayStoneInfo, setDisplayStoneInfo] = useState(false);

    const toggleDisplayStoneInfoHandler = () => {
        setDisplayStoneInfo((displayStoneInfo) => !displayStoneInfo);
    };

    return (
        <span
            className={`${styles['relative-container']} ${
                id === Number(product_id) ? styles['selected-stone'] : ''
            }`.trim()}
        >
            {displayStoneInfo && (
                <span className={styles['stone-info']}>
                    {`${color} ${stone}`}
                </span>
            )}

            <span
                onMouseEnter={toggleDisplayStoneInfoHandler}
                onMouseLeave={toggleDisplayStoneInfoHandler}
                className={styles['stones']}
            >
                <img src={image} alt={`${color}-${name}`} />
            </span>
        </span>
    );
};
