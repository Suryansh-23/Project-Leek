import { useState } from 'react';
import { HashRouter, Route, Routes } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import useHash from './useHash';
import 'primereact/resources/themes/vela-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';
import 'file-icons-js/css/style.css';
import './App.css';
import Home from './Home';
import AES from './AES';
import SideButton from './SideButton';
import SideBar from './Sidebar';
import FileVault from './FileVault';
import Stegano from './Stegano';

const App = () => {
    const [showSidebar, setShowSidebar] = useState(false);
    const [hash] = useHash();

    const pageVariants = {
        enter: {
            x: 1000,
            opacity: 0,
            scale: 0,
        },
        sidebar: {
            x: 0,
            opacity: 1,
            scale: 1,
        },
        center: {
            x: 0,
            opacity: 1,
            scale: 1,
        },
        exit: {
            x: -1000,
            opacity: 0,
            scale: 0,
        },
        transition: {
            type: 'Inertia',
            delay: 0.5,
        },
    };

    return (
        <>
            <SideButton setShowSidebar={setShowSidebar} />
            <AnimatePresence exitBeforeEnter initial={false}>
                <HashRouter>
                    <Routes>
                        <Route
                            path="/"
                            element={
                                <Home pageVariants={pageVariants} hash={hash} />
                            }
                        />
                        <Route
                            path="/aes"
                            element={
                                <AES pageVariants={pageVariants} hash={hash} />
                            }
                        />
                        <Route
                            path="/file-vault"
                            element={
                                <FileVault
                                    pageVariants={pageVariants}
                                    hash={hash}
                                />
                            }
                        />
                        <Route
                            path="/stegano"
                            element={
                                <Stegano
                                    pageVariants={pageVariants}
                                    hash={hash}
                                />
                            }
                        />
                    </Routes>
                </HashRouter>
            </AnimatePresence>
            <SideBar
                showSidebar={showSidebar}
                setShowSidebar={setShowSidebar}
            />
        </>
    );
};

export default App;
