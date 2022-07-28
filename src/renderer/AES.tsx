/* eslint-disable jsx-a11y/label-has-associated-control */
import * as React from 'react';
import { useState } from 'react';
import { AnimationProps, motion } from 'framer-motion';
import { Card } from 'primereact/card';
import { InputTextarea } from 'primereact/inputtextarea';
import { InputText } from 'primereact/inputtext';
import { Button } from 'primereact/button';
import { RadioButton } from 'primereact/radiobutton';
import { Dialog } from 'primereact/dialog';

interface AESProps {
    pageVariants: AnimationProps['variants'];
    hash: string | unknown;
}

const AES: React.FC<AESProps> = ({ pageVariants, hash }) => {
    type AesDataStruct = {
        'Cipher-Key': string;
        'Encryption-Type': string;
        'Encrypt-String': string;
        'Decrypt-String': string;
        Result: { string: string; hex: string };
        'Result-Type': string;
        'Result-Format': string;
        'Error-Messages': Array<React.ReactElement>;
    };
    const [aesData, setAesData] = useState<AesDataStruct>({
        'Cipher-Key': 'JoqCy6yyO9mU4kjM',
        'Encryption-Type': '0',
        'Encrypt-String': '',
        'Decrypt-String': '',
        Result: { string: '', hex: '' },
        'Result-Type': '',
        'Result-Format': 'string',
        'Error-Messages': [
            <>
                Either remove the string from any of these or the <br /> String
                for Decryption will be discarded.
            </>,
            <>
                The Cipher-Key being used is of incorrect Length. <br />
                Enter the correct Cipher-Key to continue.
            </>,
        ],
    });
    const [dialogVisibility, setDialogVisibility] = useState<boolean>(false);
    const encTypes = [
        { name: '128-Bit', key: '0', len: 16 },
        { name: '192-Bit', key: '1', len: 24 },
        { name: '256-bit', key: '2', len: 32 },
    ];
    const reqKeyLen = encTypes.filter(
        (i) => i.key === aesData['Encryption-Type']
    )[0].len;

    const callCipherKey = () => {
        fetch('http://127.7.3.0:2302/cipher_key', {
            headers: {
                'Encryption-Type': aesData['Encryption-Type'],
            },
        })
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                // eslint-disable-next-line no-console
                console.log(data);
                setAesData({ ...aesData, 'Cipher-Key': data });
                return true;
            })
            .catch((err) => {
                // eslint-disable-next-line no-console
                console.error(err);
                return false;
            });
    };

    const callEncrypt = () => {
        console.log(aesData);

        fetch('http://127.7.3.0:2302/aes_encryption', {
            headers: {
                'AES-String': JSON.stringify(aesData['Encrypt-String']),
                'Cipher-Key': aesData['Cipher-Key'],
                'Encryption-Type': aesData['Encryption-Type'],
            },
        })
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                // eslint-disable-next-line no-console
                console.log('Encrypt', data);
                setAesData({
                    ...aesData,
                    Result: data,
                    'Result-Type': 'Encrypted',
                });
                setDialogVisibility(true);
                return true;
            })
            .catch((err) => {
                // eslint-disable-next-line no-console
                console.error(err);
                return false;
            });
    };

    const callDecrypt = () => {
        fetch('http://127.7.3.0:2302/aes_decryption', {
            headers: {
                'AES-String': aesData['Decrypt-String'],
                'Cipher-Key': aesData['Cipher-Key'],
                'Encryption-Type': aesData['Encryption-Type'],
            },
        })
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                // eslint-disable-next-line no-console
                console.log('Decrypt', data);
                setAesData({
                    ...aesData,
                    Result: data,
                    'Result-Type': 'Decrypted',
                });
                setDialogVisibility(true);
                return true;
            })
            .catch((err) => {
                // eslint-disable-next-line no-console
                console.error(err);
                return false;
            });
    };

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
                    AES
                    <span className="project-text px-2">Encryption</span>
                </div>
            </Card>
            <Card className="border-change shadow-6">
                <div className="flex flex-column">
                    <div className="flex flex-row justify-content-around">
                        <div className="flex align-items-center">
                            Encryption
                            <i className="pi pi-lock px-1" />
                            <Button
                                icon="pi pi-copy"
                                className="blur border-change icon-btn"
                                onClick={() => {
                                    navigator.clipboard.writeText(
                                        aesData['Encrypt-String']
                                    );
                                }}
                            />
                        </div>
                        <div className="flex align-items-center">
                            Decryption
                            <i className="pi pi-lock-open px-1" />
                            <Button
                                icon="pi pi-copy"
                                className="blur border-change icon-btn"
                                onClick={() => {
                                    navigator.clipboard.writeText(
                                        aesData['Decrypt-String']
                                    );
                                }}
                            />
                        </div>
                    </div>
                    <div
                        className="flex flex-row align-items-center py-3"
                        // style={{ overflowY: 'scroll' }}
                    >
                        <span className="p-float-label flex-grow-1">
                            <InputTextarea
                                className="border-change blur"
                                value={aesData['Encrypt-String']}
                                onChange={(e) =>
                                    setAesData({
                                        ...aesData,
                                        'Encrypt-String': e.target.value,
                                    })
                                }
                                rows={10}
                                placeholder="Enter String for Encryption"
                            />
                        </span>
                        <i className="pi pi-arrows-h text-2xl m-2" />
                        <span className="p-float-label flex-grow-1">
                            <InputTextarea
                                className="border-change blur"
                                value={aesData['Decrypt-String']}
                                onChange={(e) =>
                                    setAesData({
                                        ...aesData,
                                        'Decrypt-String': e.target.value,
                                    })
                                }
                                rows={10}
                                placeholder="Enter String for Decryption"
                            />
                        </span>
                    </div>
                    <div className="text-2xl text-center mb-4">
                        Encryption Type
                        <i className="pi pi-hashtag text-2xl px-2" />
                    </div>
                    <div className="flex flex-row align-self-center mb-3">
                        {encTypes.map((type) => {
                            return (
                                <div
                                    key={type.key}
                                    className="p-field-radiobutton mr-6"
                                >
                                    <RadioButton
                                        inputId={type.key}
                                        name="category"
                                        value={type}
                                        onChange={() => {
                                            const tmp = aesData;
                                            tmp['Encryption-Type'] = type.key;
                                            setAesData(tmp);
                                            callCipherKey();
                                        }}
                                        checked={
                                            aesData['Encryption-Type'] ===
                                            type.key
                                        }
                                    />
                                    <label htmlFor={type.key}>
                                        {type.name}
                                    </label>
                                </div>
                            );
                        })}
                    </div>
                    <div
                        className={`flex flex-row align-items-center ${
                            aesData['Decrypt-String'] &&
                            aesData['Encrypt-String']
                                ? 'mb-3'
                                : 'mb-2'
                        }`}
                    >
                        <InputText
                            className="border-change blur line-height-3 webkit-width text-center"
                            value={aesData['Cipher-Key']}
                            onChange={(e) => {
                                setAesData({
                                    ...aesData,
                                    'Cipher-Key': e.target.value,
                                });
                            }}
                            placeholder="Cipher Key"
                        />
                        <Button
                            icon="pi pi-copy"
                            className="blur border-change icon-btn mr-3 -ml-5"
                            onClick={() => {
                                navigator.clipboard.writeText(
                                    aesData['Cipher-Key']
                                );
                            }}
                        />
                        <Button
                            className="button-gradient"
                            style={{ width: '15rem' }}
                            label="Generate Cipher-Key"
                            onClick={() => {
                                // console.log(aesData['Encrypt-String'] !== '');
                                callCipherKey();
                            }}
                        />
                    </div>
                    <span className="flex justify-content-center text-center p-error p-d-block">
                        {aesData['Encrypt-String'] &&
                        aesData['Decrypt-String'] ? (
                            aesData['Error-Messages'][0]
                        ) : (
                            <></>
                        )}
                        <br />
                        {aesData['Cipher-Key'].length !== reqKeyLen ? (
                            aesData['Error-Messages'][1]
                        ) : (
                            <></>
                        )}
                    </span>
                    <div className="flex justify-content-center mt-3">
                        <Button
                            className="button-gradient"
                            label={
                                aesData['Encrypt-String'] === ''
                                    ? 'Decrypt'
                                    : 'Encrypt'
                            }
                            onClick={() => {
                                if (
                                    aesData['Cipher-Key'].length !== reqKeyLen
                                ) {
                                    return;
                                }

                                if (aesData['Encrypt-String'] === '') {
                                    callDecrypt();
                                } else {
                                    callEncrypt();
                                }
                            }}
                        />
                    </div>
                </div>
                <Dialog
                    header={
                        <div className="flex align-items-center justify-content-center">
                            <span className="text-2xl ml-auto">Result</span>
                            <Button
                                icon="pi pi-copy"
                                className="blur border-change icon-btn ml-2 -mr-5"
                                onClick={() =>
                                    aesData['Result-Format'] === 'string'
                                        ? navigator.clipboard.writeText(
                                              aesData.Result.string
                                          )
                                        : navigator.clipboard.writeText(
                                              aesData.Result.hex
                                          )
                                }
                            />
                            <Button
                                icon="pi pi-times"
                                className="blur border-change icon-btn ml-auto"
                                onClick={() => setDialogVisibility(false)}
                            />
                        </div>
                    }
                    blockScroll
                    visible={dialogVisibility}
                    dismissableMask
                    closable={false}
                    style={{ width: '25rem' }}
                    onHide={() => setDialogVisibility(false)}
                >
                    <InputTextarea
                        className="border-change blur mt-2"
                        value={
                            aesData['Result-Format'] === 'string'
                                ? aesData.Result.string.replaceAll('\u0000', '')
                                : aesData.Result.hex
                        }
                        rows={10}
                        placeholder={`${aesData['Result-Type']} String`}
                        readOnly
                    />
                    <div className="flex justify-content-center mt-2">
                        <div className="p-field-radiobutton mr-6">
                            <RadioButton
                                inputId="string"
                                value="String"
                                onChange={() =>
                                    setAesData({
                                        ...aesData,
                                        'Result-Format': 'string',
                                    })
                                }
                                checked={aesData['Result-Format'] === 'string'}
                            />
                            <label htmlFor="string">String</label>
                        </div>
                        <div className="p-field-radiobutton">
                            <RadioButton
                                inputId="hex"
                                value="hex"
                                onChange={() =>
                                    setAesData({
                                        ...aesData,
                                        'Result-Format': 'hex',
                                    })
                                }
                                checked={aesData['Result-Format'] === 'hex'}
                            />
                            <label htmlFor="hex">Hexadecimal</label>
                        </div>
                    </div>
                </Dialog>
            </Card>
            <div className="pb-3" />
        </motion.div>
    );
};

export default AES;
