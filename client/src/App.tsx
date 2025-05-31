import { Header } from './components/layout/header/Header';
import { Main } from './components/layout/main/Main';

import styles from './App.module.css';

function App() {
    return (
        <div className={styles['app']}>
            <Header />
            <Main />
        </div>
    );
}

export default App;
