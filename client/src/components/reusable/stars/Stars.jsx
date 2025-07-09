import { useEffect, useState } from 'react';

import { faStar } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import styles from './Stars.module.scss';

export const Stars = ({
    rating,
    fontSize,
    interactive = false,
    onRatingChange = null,
    hoverColor = 'gold',
}) => {
    const [hoveredRating, setHoveredRating] = useState(0);
    const [selectedRating, setSelectedRating] = useState(rating || 0);

    useEffect(() => {
        setSelectedRating(rating || 0);
    }, [rating]);

    const displayRating = interactive ? hoveredRating || selectedRating : Math.floor(rating || 0);

    const handleStarClick = starIndex => {
        if (!interactive) return;

        const newRating = starIndex + 1;
        setSelectedRating(newRating);
        if (onRatingChange) {
            onRatingChange(newRating);
        }
    };

    const handleStarHover = starIndex => {
        if (!interactive) return;
        setHoveredRating(starIndex + 1);
    };

    const handleStarLeave = () => {
        if (!interactive) return;
        setHoveredRating(0);
    };

    const getStarClass = starIndex => {
        if (!interactive) {
            return starIndex < displayRating ? 'filled' : 'empty';
        }

        if (hoveredRating > 0) {
            return starIndex < hoveredRating ? `hover-${hoverColor}` : 'interactive-empty';
        }

        return starIndex < selectedRating ? 'filled' : 'interactive-empty';
    };

    return (
        <ul className={`${styles['stars']} ${interactive ? styles['interactive'] : ''}`}>
            {[...Array(5)].map((_, i) => (
                <li
                    key={i}
                    style={{
                        fontSize: fontSize ? `${fontSize}em` : `${1.2}em`,
                    }}
                    onClick={() => handleStarClick(i)}
                    onMouseEnter={() => handleStarHover(i)}
                    onMouseLeave={handleStarLeave}
                >
                    <FontAwesomeIcon icon={faStar} className={styles[getStarClass(i)]} />
                </li>
            ))}
        </ul>
    );
};
