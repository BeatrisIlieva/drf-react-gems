import { Link } from 'react-router'
import styles from './Footer.module.css'

export const Footer = () => {
    return (
        <footer className={styles['footer']}>
            <Link to='https://github.com/BeatrisIlieva/drf-react-ts-gems'>
                <span>https://github.com/BeatrisIlieva/drf-react-ts-gems</span>
            </Link>
        </footer>
    )
}