import * as React from 'react';
import { AnimationProps, motion } from 'framer-motion';
import { Card } from 'primereact/card';
import { Chip } from 'primereact/chip';
import { ipcRenderer } from 'electron';
import logo from '../../assets/icon.png';

interface HomeProps {
    pageVariants: AnimationProps['variants'];
    hash: string | unknown;
}

const Home: React.FC<HomeProps> = ({ pageVariants, hash }) => {
    // console.log('Reload', hash === '#/' ? 'sidebar' : 'enter', hash);

    return (
        <motion.div
            className="max-h-whole p-3"
            initial={hash === '#/' ? 'sidebar' : 'enter'}
            animate="center"
            exit="exit"
            variants={pageVariants}
            style={{ backgroundColor: 'var(--surface-b)' }}
        >
            <div className="flex flex-column p-2">
                <Card className="border-change shadow-6">
                    <div className="p-component text-white flex flex-column">
                        <div className="flex mx-auto align-items-center">
                            <img
                                src={logo}
                                alt="Logo"
                                className="w-8rem h-8rem"
                            />
                            <div className="text-center p-3 text-7xl line-height-2 select-none">
                                Project
                                <br />
                                <span className="project-text">Leɘk</span>
                                <span className="text-700">
                                    v
                                    {(() => {
                                        const tmp =
                                            ipcRenderer.sendSync('app-version');
                                        return tmp;
                                    })()}
                                </span>
                            </div>
                        </div>
                        <div className="text-center font-italic text-4xl line-height-1 p-2">
                            <span className="project-text">Secrets</span> are
                            not to be
                            <span className="project-text"> Shared</span>
                            {/* <span className="project-text">Crypto</span>{' '}
                            Ain&apos;t always{' '}
                            <span className="project-text">Cryptocurrency</span> */}
                        </div>
                    </div>
                </Card>
                <Card className="border-change align-self-center absolute bottom-0 mb-5 shadow-6">
                    <div className="flex flex-column">
                        <div className="align-self-center pb-2">
                            <a
                                title="github"
                                className="appearance-none p-2"
                                href="https://github.com/Suryansh-23/Project-Leek"
                                rel="noreferrer noopener"
                                target="_blank"
                            >
                                <Chip
                                    label="Github"
                                    icon="pi pi-github"
                                    className="bg-project p-mr-2 p-mb-2 blur"
                                />
                            </a>
                            <a
                                title="wiki"
                                className="appearance-none"
                                href="https://en.wikipedia.org/wiki/Advanced_Encryption_Standard"
                                rel="noreferrer noopener"
                                target="_blank"
                            >
                                <Chip
                                    label="Wikipedia"
                                    icon="pi icon-wiki"
                                    className="bg-project p-mr-2 p-mb-2 blur"
                                />
                            </a>
                        </div>
                        Know More about What You&apos;re Using
                    </div>
                </Card>
            </div>
        </motion.div>
    );
};

export default React.memo(Home);
