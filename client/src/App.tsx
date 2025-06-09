import { Header } from './components/layout/header/Header';
import { Main } from './components/layout/main/Main';

import styles from './App.module.scss';
import { ScrollToTop } from './components/layout/scroll-to-top/ScrollToTop';

function App() {
    return (
        <div className={styles['app']}>
            <Header />
            <Main />
            <ScrollToTop />
        </div>
    );
}

export default App;
