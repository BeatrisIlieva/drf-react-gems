import { Link } from 'react-router';
import styles from './Footer.module.css';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGithub } from '@fortawesome/free-brands-svg-icons';
import { faLinkedin } from '@fortawesome/free-brands-svg-icons';
import { faEnvelope } from '@fortawesome/free-solid-svg-icons';

export const Footer = () => {
    return (
        <footer className={styles['footer']}>
            <h5>connect with us</h5>
            <Link to='https://github.com/BeatrisIlieva'>
                <FontAwesomeIcon icon={faGithub} />
                <span>https://github.com/BeatrisIlieva</span>
            </Link>
            <Link to='https://www.linkedin.com/in/beatrisilieva'>
                <FontAwesomeIcon icon={faLinkedin} />
                <span>https://www.linkedin.com/in/beatrisilieva</span>
            </Link>
            <span>
                <FontAwesomeIcon icon={faEnvelope} />
                <span>beatris.ilieva@icloud.com</span>
            </span>
        </footer>
    );
};
