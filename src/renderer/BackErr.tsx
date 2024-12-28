import * as React from 'react';

const BackErr: React.FC = () => {
    console.log('FOFF BackErr');

    return (
        <div className="flex flex-row max-w-full my-auto">
            <i
                className="pi pi-exclamation-triangle text-8xl"
                style={{ color: 'red' }}
            />
            <h1>F U</h1>
        </div>
    );
};

export default BackErr;
