import * as React from 'react';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const useHash: () => (string | ((newHash: any) => void) | null)[] = () => {
    const [hash, setHash] = React.useState<string | null>(
        () => window.location.hash
    );

    const hashChangeHandler = React.useCallback(() => {
        setHash(window.location.hash);
    }, []);

    React.useEffect(() => {
        window.addEventListener('hashchange', hashChangeHandler);
        return () => {
            window.removeEventListener('hashchange', hashChangeHandler);
        };
    }, [hashChangeHandler]);

    const updateHash = React.useCallback(
        (newHash) => {
            if (newHash !== hash) window.location.hash = newHash;
        },
        [hash]
    );

    return [hash, updateHash];
};

export default useHash;
