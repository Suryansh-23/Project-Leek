/* eslint-disable no-restricted-syntax */
/* eslint-disable @typescript-eslint/ban-types */
/* eslint-disable @typescript-eslint/naming-convention */
import * as React from 'react';
import { useState, useEffect, useRef } from 'react';
import { motion, AnimationProps } from 'framer-motion';
import { Card } from 'primereact/card';
import {
    FileUpload,
    FileUploadHeaderTemplateOptions,
    FileUploadUploadParams,
} from 'primereact/fileupload';
import { ProgressBar } from 'primereact/progressbar';
// import { Button } from 'primereact/button';
// import { Tag } from 'primereact/tag';
import locker from '../../assets/locker.svg';

interface FileVaultProps {
    pageVariants: AnimationProps['variants'];
    hash: string | unknown;
}

const FileVault: React.FC<FileVaultProps> = ({ pageVariants, hash }) => {
    const [totalSize, setTotalSize] = useState<Number>(0);
    const fileUploadRef = useRef(null);

    useEffect(() => {
        const el = document.querySelector('input[type="file"]');
        if (el != null) {
            el.setAttribute('webkitdirectory', '');
            el.setAttribute('directory', '');
        }
    }, []);

    const onTemplateUpload = (e: FileUploadUploadParams) => {
        let tempSize = 0;
        e.file.forEach((f) => {
            tempSize += f.size || 0;
            // eslint-disable-next-line no-console
            console.log(f);
        });
        setTotalSize(tempSize);
        console.log('tempSize', totalSize);
    };

    const headerTemplate: React.FC<FileUploadHeaderTemplateOptions> = (
        options
    ) => {
        const { className, chooseButton, uploadButton, cancelButton } = options;
        let value = 0;
        if (fileUploadRef.current && fileUploadRef.current.files) {
            const { files } = fileUploadRef.current;
            for (const i of files) {
                value += i.size / 1000000;
            }
        }
        setTotalSize(Math.round(value));
        console.log(fileUploadRef.current, value, totalSize);
        return (
            <div
                className={className}
                style={{
                    backgroundColor: 'transparent',
                    display: 'flex',
                    alignItems: 'center',
                }}
            >
                {chooseButton}
                {uploadButton}
                {cancelButton}
                <ProgressBar
                    value={Number(totalSize)}
                    displayValueTemplate={() => `${totalSize} / 128 MB`}
                    style={{
                        width: '300px',
                        height: '30px',
                        marginLeft: 'auto',
                    }}
                />
            </div>
        );
    };

    return (
        <motion.div
            className="p-3 max-h-whole"
            initial={hash === '#/file-vault' ? 'sidebar' : 'enter'}
            animate="center"
            exit="exit"
            variants={pageVariants}
            style={{ backgroundColor: 'var(--surface-b)' }}
        >
            <Card className="border-change shadow-6 mb-5">
                <div className="flex flex-row p-2 text-center text-white text-6xl justify-content-center align-items-center">
                    <img
                        src={locker}
                        className="locker-logo px-3"
                        alt="File-Vault Logo"
                    />
                    File
                    <span className="project-text px-2">Vault</span>
                </div>
            </Card>
            <Card className="border-change shadow-6 mb-5">
                <FileUpload
                    name="demo[]"
                    multiple
                    accept="/*"
                    ref={fileUploadRef}
                    maxFileSize={128000000 - Number(totalSize)}
                    onUpload={onTemplateUpload}
                    headerTemplate={headerTemplate}
                    onClear={() => {
                        console.log('Cleared');
                        setTotalSize(0);
                        fileUploadRef.current.files = [];
                        console.log(totalSize);
                    }}
                    onRemove={(e) => {
                        let tmpFiles = Array.from(fileUploadRef.current.files);
                        let i = 0;
                        for (const item of tmpFiles) {
                            if (item === e.file) {
                                break;
                            }
                            i += 1;
                        }
                        tmpFiles = [
                            ...tmpFiles.slice(0, i),
                            ...tmpFiles.slice(i + 1),
                        ];
                        console.log('New Files', tmpFiles, e.file);
                        fileUploadRef.current.files = tmpFiles;
                    }}
                    emptyTemplate={
                        <p className="p-m-0">
                            Drag and drop files to here to upload.
                        </p>
                    }
                />
            </Card>
        </motion.div>
    );
};

export default FileVault;
