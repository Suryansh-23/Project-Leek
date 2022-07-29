/* eslint-disable no-console */
import * as React from 'react';
import { useRef, useEffect } from 'react';
import { Tag } from 'primereact/tag';

const TestResult: React.FunctionComponent = () => {
    const tests: {
        api?: boolean;
        cipher_key?: boolean;
        aes: boolean;
        file_vault?: boolean;
        steganography: boolean;
    } = { aes: true, cipher_key: true, steganography: true };
    const testsRef = useRef(tests);

    useEffect(() => {
        const testCipherKey: Array<string> = [];
        const testString = 'Hello\nWorld';
        const testEncryptedStrings: Array<string> = [];

        // Checks whether the API is up or not via hitting its main route
        fetch('http://127.7.3.0:2302/')
            .then((response) => {
                if (response.ok) {
                    testsRef.current.api = true;
                } else {
                    testsRef.current.api = false;
                }
                return true;
            })
            .catch((err) => {
                // eslint-disable-next-line no-console
                console.error(err);
                testsRef.current.api = false;
                return false;
            });

        // Checks whether the API endpoint for generating Cipher-Keys is Up or not.And, also stores the keys generated for AES Testing
        [0, 1, 2].forEach((i) => {
            let key: string;
            let enStr: string;
            fetch('http://127.7.3.0:2302/cipher_key', {
                headers: {
                    'Encryption-Type': String(i),
                },
            })
                .then((response) => {
                    if (!response.ok) {
                        testsRef.current.cipher_key = false;
                        throw Error();
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data !== '' && data.length === 16 + 8 * i) {
                        testsRef.current.cipher_key &&= true;
                        testCipherKey.push(data);
                        key = data;
                        return data;
                    }
                    return data;
                })
                // Generates the AES Encrypted String for Each Cipher-Key generated previously and stores them for future comparison
                .finally(() => {
                    fetch('http://127.7.3.0:2302/aes_encryption', {
                        headers: {
                            'AES-String': JSON.stringify(testString),
                            // 'Cipher-Key': String(testCipherKey.at(-1)),
                            'Cipher-Key': key,
                            'Encryption-Type': String(i),
                        },
                    })
                        .then((response) => {
                            if (!response.ok) {
                                throw Error();
                            }
                            return response.json();
                        })
                        .then((data) => {
                            console.log(`${i} ${data.hex}`);
                            enStr = data.hex;
                            testEncryptedStrings.push(data.hex);
                            return true;
                        })
                        // Compares whether the decrypted string match the orignal string by using the AES Decryption API Endpoint
                        .finally(() => {
                            fetch('http://127.7.3.0:2302/aes_decryption', {
                                headers: {
                                    // 'AES-String': String(testEncryptedStrings.at(-1)),
                                    'AES-String': enStr,
                                    // 'Cipher-Key': String(testCipherKey.at(-1)),
                                    'Cipher-Key': key,
                                    'Encryption-Type': String(i),
                                },
                            })
                                .then((response) => {
                                    if (!response.ok) {
                                        testsRef.current.aes = false;
                                        throw Error();
                                    }
                                    return response.json();
                                })
                                .then((data) => {
                                    console.log(`${i} ${data.string}`);
                                    if (data.string === testString) {
                                        testsRef.current.aes &&= true;
                                        return true;
                                    }

                                    return false;
                                })
                                .catch((err) => {
                                    // eslint-disable-next-line no-console
                                    console.error(err);
                                    testsRef.current.aes = false;
                                    return false;
                                });
                        })
                        .catch((err) => {
                            // eslint-disable-next-line no-console
                            console.error(err);
                            testEncryptedStrings.push('');
                            return false;
                        });
                })
                .catch((err) => {
                    // eslint-disable-next-line no-console
                    console.error(err);
                    testsRef.current.cipher_key = false;
                    return false;
                });
        });

        // Uses Inverse Testing by not providing the required headers and then checks if the returned result is the optimum case
        fetch('http://127.7.3.0:2302/file_vault')
            .then((response) => {
                if (!response.ok && response.status === 500) {
                    testsRef.current.file_vault = true;
                } else {
                    testsRef.current.file_vault = false;
                }
                return true;
            })
            .catch((err) => {
                // eslint-disable-next-line no-console
                console.error(err);
                return false;
            });

        // Compares whether the decrypted string match the orignal string by using the AES Decryption API Endpoint
        testsRef.current.aes = testEncryptedStrings
            .map((i, ind) => {
                let check;
                fetch('http://127.7.3.0:2302/aes_decryption', {
                    headers: {
                        'AES-String': JSON.stringify(i),
                        'Cipher-Key': testCipherKey[ind],
                        'Encryption-Type': String(ind),
                    },
                })
                    .then((response) => {
                        if (!response.ok) {
                            throw Error();
                        }
                        return response.json();
                    })
                    .then((data) => {
                        if (data.string === testString) {
                            check = true;
                        }

                        return true;
                    })
                    .catch((err) => {
                        // eslint-disable-next-line no-console
                        console.error(err);
                        check = false;
                        return false;
                    });

                return check;
            })
            .every((i) => i === true);

        console.log(testsRef.current);
    }, [testsRef]);

    return (
        <div className="flex flex-column mt-3 align-items-center">
            <strong className="text-xl font-bold mb-3">
                Diagnostic Checks
            </strong>
            <Tag
                className="mb-2 w-min text-white border-change"
                style={{
                    backgroundColor: testsRef.current.api ? 'green' : 'crimson',
                }}
                icon={`pi ${testsRef.current.api ? 'pi-check' : 'pi-times'}`}
                // severity="danger"
                value="API"
            />
            <Tag
                className="mb-2 w-min text-white border-change nowrap"
                style={{
                    backgroundColor: testsRef.current.cipher_key
                        ? 'green'
                        : 'crimson',
                }}
                icon={`pi ${
                    testsRef.current.cipher_key ? 'pi-check' : 'pi-times'
                }`}
                // severity="danger"
                value="Cipher Key"
            />
            <Tag
                className="mb-2 w-min text-white border-change"
                style={{
                    backgroundColor: testsRef.current.aes ? 'green' : 'crimson',
                }}
                icon={`pi ${testsRef.current.aes ? 'pi-check' : 'pi-times'}`}
                // severity="danger"
                value="AES"
            />
            <Tag
                className="mb-2 w-min text-white border-change nowrap"
                style={{
                    backgroundColor: testsRef.current.file_vault
                        ? 'green'
                        : 'crimson',
                }}
                icon={`pi ${
                    testsRef.current.file_vault ? 'pi-check' : 'pi-times'
                }`}
                // severity="danger"
                value="File Vault"
            />
            <Tag
                className="mb-2 w-min text-white border-change nowrap"
                style={{
                    backgroundColor: testsRef.current.steganography
                        ? 'green'
                        : 'crimson',
                }}
                icon={`pi ${
                    testsRef.current.steganography ? 'pi-check' : 'pi-times'
                }`}
                // severity="danger"
                value="Steganography"
            />
        </div>
    );
};

export default TestResult;
