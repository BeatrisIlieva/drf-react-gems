import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStar } from '@fortawesome/free-solid-svg-icons';
import styles from './Stars.module.css';

export const Stars = ({ rating }) => {
    const roundedRating = Math.round(rating);

    return (
        <ul className={styles['stars']}>
            {[...Array(5)].map((_, i) => (
                <li key={i}>
                    <FontAwesomeIcon
                        icon={faStar}
                        className={styles[i < roundedRating ? 'filled' : 'empty']}
                    />
                </li>
            ))}
        </ul>
    );
};
