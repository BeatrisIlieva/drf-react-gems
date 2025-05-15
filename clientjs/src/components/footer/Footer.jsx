import { Link } from 'react-router';
import styles from './Footer.module.css';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGithub } from '@fortawesome/free-brands-svg-icons';
import {
    faLinkedin,
    faDev,
    faYoutube
} from '@fortawesome/free-brands-svg-icons';
import { faEnvelope } from '@fortawesome/free-solid-svg-icons';

export const Footer = () => {
    return (
        <footer className={styles['footer']}>
            <h5>connect with us</h5>
            <div className={styles['wrapper']}>
                <div className={styles['thumbnail']}>
                    <Link
                        to='https://github.com/BeatrisIlieva'
                        className={styles['icon']}
                    >
                        <FontAwesomeIcon icon={faGithub} />
                    </Link>
                </div>
                <div className={styles['thumbnail']}>
                    <Link
                        to='https://www.linkedin.com/in/beatrisilieva'
                        className={styles['icon']}
                    >
                        <FontAwesomeIcon icon={faLinkedin} />
                    </Link>
                </div>
                <div className={styles['thumbnail']}>
                    <Link
                        to='https://www.linkedin.com/in/beatrisilieva'
                        className={styles['icon']}
                    >
                        <FontAwesomeIcon icon={faDev} />
                    </Link>
                </div>
                <div className={styles['thumbnail']}>
                    <Link
                        to='https://www.linkedin.com/in/beatrisilieva'
                        className={styles['icon']}
                    >
                        <FontAwesomeIcon icon={faYoutube} />
                    </Link>
                </div>
            </div>

            <span>
                <FontAwesomeIcon icon={faEnvelope} />
                <span>beatris.ilieva@icloud.com</span>
            </span>
        </footer>
    );
};
