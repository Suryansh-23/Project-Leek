import * as React from 'react';
import { useState, useRef } from 'react';
import { motion, AnimationProps } from 'framer-motion';
import { Card } from 'primereact/card';
import { FileUpload } from 'primereact/fileupload';
import { Button } from 'primereact/button';
import { Tag } from 'primereact/tag';
import { InputText } from 'primereact/inputtext';
import { InputTextarea } from 'primereact/inputtextarea';

interface SteganoProps {
    pageVariants: AnimationProps['variants'];
    hash: string | unknown;
}

const Stegano: React.FC<SteganoProps> = ({ pageVariants, hash }) => {
    const [totalSize, setTotalSize] = useState<number>(0);
    const [privateKey, setPrivateKey] = useState<string>('');
    const [msg, setMsg] = useState<string>('');
    const fileUploadRef = useRef<null | FileUpload>(null);
    const toast = useRef(null);

    const onTemplateSelect = (e) => {
        let tmpTotalSize = totalSize;
        Array.from(e.files).forEach((file) => {
            tmpTotalSize += file.size;
        });
        setTotalSize(tmpTotalSize);
    };

    const onTemplateUpload = (e) => {
        let tmpTotalSize = 0;
        Array.from(e.files).forEach((file) => {
            tmpTotalSize += file.size || 0;
        });

        setTotalSize(tmpTotalSize);
        toast.current.show({
            severity: 'info',
            summary: 'Success',
            detail: 'File Uploaded',
        });
    };

    const onTemplateRemove = (file, callback) => {
        setTotalSize(totalSize - file.size);
        callback();
    };

    const onTemplateClear = () => {
        setTotalSize(0);
    };

    const headerTemplate = (options) => {
        const { className, chooseButton, uploadButton, cancelButton } = options;

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
            </div>
        );
    };

    const itemTemplate = (file, props) => {
        return (
            <div className="flex align-items-center flex-wrap">
                <img
                    alt={file.name}
                    role="presentation"
                    src={file.objectURL}
                    width={300}
                />
                <div
                    className="flex align-items-center"
                    // style={{ width: '40%' }}
                >
                    <span className="flex flex-column text-left ml-3">
                        {file.name}
                        <small>{new Date().toLocaleDateString()}</small>
                    </span>
                </div>
                <Tag
                    value={props.formatSize}
                    severity="warning"
                    className="border-change ml-auto px-3 py-2"
                />
                <Button
                    type="button"
                    icon="pi pi-times"
                    className="p-button-outlined p-button-rounded p-button-danger file-remove border-change ml-auto"
                    onClick={() => onTemplateRemove(file, props.onRemove)}
                />
            </div>
        );
    };

    const emptyTemplate = () => {
        return (
            <div className="flex align-items-center flex-column">
                <i
                    className="pi pi-image mt-3 p-5"
                    style={{
                        fontSize: '5em',
                        borderRadius: '50%',
                        backgroundColor: 'var(--surface-b)',
                        color: 'var(--surface-d)',
                    }}
                />
                <span
                    style={{
                        fontSize: '1.2em',
                        color: 'var(--text-color-secondary)',
                    }}
                    className="my-5"
                >
                    Drag and Drop Image Here
                </span>
            </div>
        );
    };

    const chooseOptions = {
        label: 'Add Image',
        icon: 'pi pi-fw pi-image',
        className: 'button-gradient p-button-oulined',
    };
    const uploadOptions = {
        icon: 'pi pi-fw pi-cloud-upload',
        iconOnly: true,
        className: 'button-gradient p-button-outlined',
    };
    const cancelOptions = {
        icon: 'pi pi-fw pi-times',
        iconOnly: true,
        className: 'button-gradient p-button-outlined',
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
                    <span className="project-text">Stegano</span>
                    graphy
                </div>
            </Card>
            <div className="flex flex-row">
                <Card
                    className="border-change shadow-6 mr-3"
                    style={{ width: '-webkit-fill-available' }}
                >
                    <FileUpload
                        ref={fileUploadRef}
                        name="demo[]"
                        accept="image/*"
                        maxFileSize={1000000}
                        style={{ width: '-webkit-fill-available' }}
                        onUpload={onTemplateUpload}
                        onSelect={onTemplateSelect}
                        onError={onTemplateClear}
                        onClear={onTemplateClear}
                        headerTemplate={headerTemplate}
                        itemTemplate={itemTemplate}
                        progressBarTemplate={<></>}
                        emptyTemplate={emptyTemplate}
                        chooseOptions={chooseOptions}
                        uploadOptions={uploadOptions}
                        cancelOptions={cancelOptions}
                    />
                </Card>
                <Card
                    className="border-change shadow-6 w-5"
                    style={{ height: 'fit-content' }}
                >
                    <InputTextarea
                        className="border-change blur mb-3"
                        placeholder="Enter Message"
                        value={msg}
                        onChange={(e) => setMsg(e.target.value)}
                        rows={10}
                    />
                    <InputText
                        className="border-change blur line-height-3"
                        value={privateKey}
                        onChange={(e) => setPrivateKey(e.target.value)}
                        placeholder="Enter Private Key"
                        style={{ width: '-webkit-fill-available' }}
                    />
                    <div className="flex justify-content-center pb-3 mt-3">
                        <Button
                            className={`button-gradient ${
                                privateKey && (totalSize > 0 || msg !== '')
                                    ? ''
                                    : 'p-disabled'
                            }`}
                            label={totalSize ? 'Decode' : 'Encode'}
                        />
                    </div>
                </Card>
            </div>
        </motion.div>
    );
};

export default Stegano;
