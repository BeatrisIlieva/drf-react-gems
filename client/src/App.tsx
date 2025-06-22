import { Header } from './components/layout/header/Header';
import { Main } from './components/layout/main/Main';

import styles from './App.module.scss';
import { ScrollToTop } from './components/layout/scroll-to-top/ScrollToTop';
import { Footer } from './components/layout/footer/Footer';

function App() {
    return (
        <div className={styles['app']}>
            <Header />
            <Main />
            <ScrollToTop />
            <Footer />
        </div>
    );
}

export default App;
