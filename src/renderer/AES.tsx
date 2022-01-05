/* eslint-disable jsx-a11y/label-has-associated-control */
import * as React from 'react';
import { useState } from 'react';
import { AnimationProps, motion } from 'framer-motion';
import { Card } from 'primereact/card';
import { InputTextarea } from 'primereact/inputtextarea';
import { InputText } from 'primereact/inputtext';
import { Button } from 'primereact/button';

interface AESProps {
    pageVariants: AnimationProps['variants'];
    hash: string | unknown;
}

const AES: React.FC<AESProps> = ({ pageVariants, hash }) => {
    const [encryptStr, setEncryptStr] = useState<string>('');
    const [decryptStr, setDecryptStr] = useState<string>('');
    const [privateKey, setPrivateKey] = useState<string>('');

    return (
        <motion.div
            className="p-3 max-h-whole"
            initial={hash === '#/aes' ? 'sidebar' : 'enter'}
            animate="center"
            exit="exit"
            variants={pageVariants}
            style={{ backgroundColor: 'var(--surface-b)' }}
        >
            <Card className="border-change shadow-6 mb-5 p-2">
                <div className="flex flex-row p-2 text-center text-white text-6xl justify-content-center">
                    AES-128 Bit
                    <span className="project-text px-2">Encryption</span>
                </div>
            </Card>
            <Card className="border-change shadow-6">
                <div className="flex flex-column">
                    <div
                        className={`flex flex-row justify-content-around pb-${
                            encryptStr || decryptStr ? 4 : 0
                        }`}
                    >
                        <div>
                            Encryption
                            <i className="pi pi-lock px-1" />
                        </div>
                        <div>
                            Decryption
                            <i className="pi pi-lock-open px-1" />
                        </div>
                    </div>
                    <div
                        className="flex flex-row align-items-center py-3"
                        // style={{ overflowY: 'scroll' }}
                    >
                        <span className="p-float-label flex-grow-1">
                            <InputTextarea
                                className="border-change blur"
                                value={encryptStr}
                                onChange={(e) => setEncryptStr(e.target.value)}
                                rows={10}
                            />
                            <label htmlFor="in">
                                Enter String for Encryption
                            </label>
                        </span>
                        <i className="pi pi-arrows-h text-2xl m-2" />
                        <span className="p-float-label flex-grow-1">
                            <InputTextarea
                                className="border-change blur"
                                value={decryptStr}
                                onChange={(e) => setDecryptStr(e.target.value)}
                                rows={10}
                            />

                            <label htmlFor="in">
                                Enter String for Decryption
                            </label>
                        </span>
                    </div>
                    <div className="flex justify-content-center pb-3">
                        <Button
                            className="button-gradient"
                            label={encryptStr === '' ? 'Decrypt' : 'Encrypt'}
                        />
                    </div>
                    <InputText
                        className={`border-change blur line-height-3 ${
                            decryptStr && encryptStr ? 'mb-3' : 'mb-2'
                        }`}
                        value={privateKey}
                        onChange={(e) => setPrivateKey(e.target.value)}
                        placeholder="Enter Private Key"
                    />
                    {encryptStr && decryptStr ? (
                        <span className="flex justify-content-center text-center p-error p-d-block">
                            Either remove the string from any of these or the
                            <br />
                            String for Decryption will be overwritten.
                        </span>
                    ) : (
                        <></>
                    )}
                </div>
            </Card>
        </motion.div>
    );
};

export default AES;
