import * as React from 'react';
import { useRef, useEffect } from 'react';
import { AnimationProps, motion } from 'framer-motion';
import { Card } from 'primereact/card';
import { ipcRenderer } from 'electron';
import { Chip } from 'primereact/chip';
import { Avatar } from 'primereact/avatar';
import logo from '../../assets/icon.png';
import TestResult from './TestResult';

interface AboutProps {
    pageVariants: AnimationProps['variants'];
    hash: string | unknown;
}

const About: React.FC<AboutProps> = ({ pageVariants, hash }) => {
    const tags = [
        'Electron',
        'React',
        'Javascript',
        'Desktop App',
        'Python',
        'Cryptography',
        'Privacy',
        'Typescript',
        'JS',
        'TS',
        'Steganography',
        'AES Encryption',
        'File Encryption',
        'File Vault',
        'String Encryption',
    ];
    const avatarImg: Array<{
        username: string;
        name: string;
        url: string;
        src: string;
    }> = [
        {
            username: 'Suryansh-23',
            name: 'Suryansh Chauhan',
            url: 'https://github.com/Suryansh-23/',
            src: 'https://avatars.githubusercontent.com/u/72202812?v=4',
        },
        {
            username: 'PouchCotato',
            name: 'Akshar Agrawal',
            url: 'https://github.com/PouchCotato/',
            src: 'https://avatars.githubusercontent.com/u/83448183?v=4',
        },
    ];
    const avatarRef = useRef(avatarImg);

    useEffect(() => {
        const main: Array<{
            username: string;
            name: string;
            url: string;
            src: string;
        }> = [];

        avatarRef.current.forEach((i) =>
            fetch(i.src)
                .then((respose) => {
                    return respose.blob();
                })
                .then((blob) => {
                    const src = URL.createObjectURL(blob);
                    main.push({ src, ...i });
                    return src;
                })
                .catch((err) => {
                    throw new Error(err);
                })
        );

        avatarRef.current = main;
    }, [avatarRef]);

    return (
        <motion.div
            className="max-h-whole p-3"
            initial={hash === '#/' ? 'sidebar' : 'enter'}
            animate="center"
            exit="exit"
            variants={pageVariants}
            style={{ backgroundColor: 'var(--surface-b)' }}
        >
            <Card className="border-change shadow-6 mb-5 p-2">
                <div className="flex flex-row p-2 text-center text-white text-6xl justify-content-center">
                    About
                    <span className="project-text px-2">The App</span>
                </div>
            </Card>
            <Card className="border-change shadow-6 text-center">
                <span className="text-5xl select-none">
                    Project
                    <span className="project-text"> Leɘk</span>
                </span>
                <div className="w-full px-4 mt-3">
                    <div
                        className="flex flex-row mx-auto relative"
                        style={{ maxWidth: '45rem' }}
                    >
                        <div className="flex flex-column w-max">
                            <img
                                src={logo}
                                alt="Logo"
                                className="w-12rem h-12rem p-2 bg-black-alpha-40 border-change"
                            />
                            <TestResult />
                        </div>
                        <div className="flex flex-column w-full pl-4">
                            <div className="grid pt-2">
                                <strong className="col-fixed w-10rem text-xl project-text text-right pr-1 font-bold nowrap">
                                    Version No.
                                </strong>
                                <p className="col m-0 text-left">
                                    v
                                    {(() => {
                                        const tmp =
                                            ipcRenderer.sendSync('app-version');
                                        return tmp;
                                    })()}
                                </p>
                            </div>
                            <div className="grid pt-2">
                                <strong className="col-fixed w-10rem text-xl project-text text-right pr-1 font-bold nowrap">
                                    License
                                </strong>
                                <p className="col m-0 text-left">MIT</p>
                            </div>
                            <div className="grid pt-2">
                                <strong className="col-fixed w-10rem text-xl project-text text-right pr-1 font-bold nowrap">
                                    Description
                                </strong>
                                <p className="col m-0 text-left">
                                    An AES based smart cryptographic desktop app
                                    that can help users keep their data private.
                                    It provides String, File Encryption and
                                    Image Steganography 🧑🏻‍💻😁🦄📂📷
                                </p>
                            </div>

                            <div className="grid pt-3">
                                <strong className="col-fixed w-10rem text-xl project-text text-right pr-1 font-bold nowrap">
                                    Contributors
                                </strong>
                                <div className="flex flex-column">
                                    {avatarImg.map((i) => {
                                        return (
                                            <a
                                                key={i.username}
                                                title={i.username}
                                                className="appearance-none"
                                                href={i.url}
                                                rel="noreferrer noopener"
                                                target="_blank"
                                            >
                                                <Card className="border-change mb-2 blur">
                                                    <div className="flex flex-row">
                                                        <Avatar
                                                            image={i.src}
                                                            className="mr-2 avatar-xxl"
                                                            shape="circle"
                                                        />
                                                        <div className="my-auto">
                                                            <span className="text-2xl">
                                                                @{i.username}
                                                            </span>
                                                            <br />
                                                            <span className="text-700 text-lg">
                                                                {i.name}
                                                            </span>
                                                        </div>
                                                    </div>
                                                </Card>
                                            </a>
                                        );
                                    })}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="flex flex-wrap w-9 mt-3 mx-auto justify-content-center">
                        {tags.map((i) => {
                            return (
                                <Chip label={i} key={i} className="blur mr-1" />
                            );
                        })}
                    </div>
                </div>
            </Card>
        </motion.div>
    );
};

export default About;
