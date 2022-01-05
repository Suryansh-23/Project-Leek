import * as React from 'react';
import { motion } from 'framer-motion';

interface SideButtonProps {
    setShowSidebar: React.Dispatch<React.SetStateAction<boolean>>;
}

const SideButton: React.FC<SideButtonProps> = ({ setShowSidebar }) => {
    return (
        <motion.div
            drag="x"
            dragSnapToOrigin
            dragConstraints={{ left: 0, right: 100 }}
            dragElastic={0.2}
            className="absolute top-50 left-0"
            style={{ transform: 'translateY(-1rem)' }}
            onDragStart={() => setShowSidebar(true)}
        >
            <div
                className="h-5rem border-round bg-white flex flex-column justify-content-center text-black ml-1"
                style={{ width: '0.4rem' }}
            />
        </motion.div>
    );
};

export default SideButton;
