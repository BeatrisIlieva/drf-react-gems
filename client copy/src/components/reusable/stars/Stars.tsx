import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStar } from '@fortawesome/free-solid-svg-icons';
import styles from './Stars.module.scss';

interface Props {
    rating: number;
    fontSize?: number;
}

export const Stars = ({ rating, fontSize }: Props) => {
    const roundedRating = Math.floor(rating);

    return (
        <ul className={styles['stars']}>
            {[...Array(5)].map((_, i) => (
                <li
                    key={i}
                    style={{
                        fontSize: fontSize ? `${fontSize}em` : `${1.2}em`
                    }}
                >
                    <FontAwesomeIcon
                        icon={faStar}
                        className={styles[i < roundedRating ? 'filled' : 'empty']}
                    />
                </li>
            ))}
        </ul>
    );
};
