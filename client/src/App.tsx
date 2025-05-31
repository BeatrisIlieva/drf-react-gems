import { Header } from './components/layout/header/Header';
import { Main } from './components/layout/main/Main';

import styles from './App.module.scss';

function App() {
    return (
        <div className={styles['app']}>
            <div className={styles['header-wrapper']}>
                <Header />
            </div>
            <Main />
        </div>
    );
}

export default App;
