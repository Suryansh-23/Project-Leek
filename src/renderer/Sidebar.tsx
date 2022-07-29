import * as React from 'react';
import { Sidebar } from 'primereact/sidebar';
import { Menu } from 'primereact/menu';

interface SideBarProps {
    showSidebar: boolean;
    setShowSidebar: React.Dispatch<React.SetStateAction<boolean>>;
}

const SideBar: React.FC<SideBarProps> = ({ showSidebar, setShowSidebar }) => {
    const items = [
        {
            label: 'Home',
            icon: 'pi pi-home',
            className: 'flex-1 justify-content-center sidebar-home',
            command: () => {
                window.location.hash = '#/';
                setShowSidebar(false);
            },
        },
        {
            label: 'String Encryption',
            items: [
                {
                    label: 'AES Encryption',
                    icon: 'pi pi-key',
                    command: () => {
                        window.location.hash = '#/aes';
                        setShowSidebar(false);
                    },
                },
            ],
        },
        {
            label: 'Data Encryption',
            items: [
                {
                    label: 'File Vault',
                    icon: 'pi pi-lock',
                    command: () => {
                        window.location.hash = '#/file-vault';
                        setShowSidebar(false);
                    },
                },
            ],
        },
        {
            label: 'Embedded Encryption',
            items: [
                {
                    label: 'Steganography',
                    icon: 'pi pi-image',
                    command: () => {
                        window.location.hash = '#/stegano';
                        setShowSidebar(false);
                    },
                },
            ],
        },
        {
            label: 'About',
            icon: 'pi pi-info-circle',
            className: 'flex-1 justify-content-center sidebar-home',
            command: () => {
                window.location.hash = '#/about';
                setShowSidebar(false);
            },
        },
    ];

    return (
        <div className="flex">
            <Sidebar
                visible={showSidebar}
                position="left"
                className="max-w-max blur sidebar-radius"
                showCloseIcon={false}
                onHide={() => setShowSidebar(false)}
                appendTo={document.getElementById('root')}
            >
                <div className="text-center p-3 text-6xl line-height-2 select-none">
                    Project
                    <br />
                    <span className="project-text">Leɘk</span>
                </div>
                <Menu className="w-full" model={items} />
            </Sidebar>
        </div>
    );
};

export default SideBar;
