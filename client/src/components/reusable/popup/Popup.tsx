import { useEffect, useRef, type ReactElement, type ReactNode } from 'react';
import { Icon } from '../icon/Icon';
import styles from './Popup.module.scss';

interface PopupProps {
    isOpen: boolean;
    onClose: () => void;
    children: ReactNode;
}

export const Popup = ({ isOpen, onClose, children }: PopupProps): ReactElement | null => {
    const popupRef = useRef<HTMLDivElement>(null);
    const overlayRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const handleEscapeKey = (event: KeyboardEvent) => {
            if (event.key === 'Escape') {
                onClose();
            }
        };

        const handleClickOutside = (event: MouseEvent) => {
            if (overlayRef.current && event.target === overlayRef.current) {
                onClose();
            }
        };

        if (isOpen) {
            document.addEventListener('keydown', handleEscapeKey);
            document.addEventListener('mousedown', handleClickOutside);
            document.body.style.overflow = 'hidden';
        }

        return () => {
            document.removeEventListener('keydown', handleEscapeKey);
            document.removeEventListener('mousedown', handleClickOutside);
            document.body.style.overflow = 'unset';
        };
    }, [isOpen, onClose]);

    if (!isOpen) {
        return null;
    }

    return (
        <div className={styles.overlay} ref={overlayRef}>
            <div className={styles.popup} ref={popupRef}>
                <button 
                    className={styles.closeButton}
                    onClick={onClose}
                    aria-label="Close popup"
                >
                    <Icon name="xMark" fontSize={0.9}/>
                </button>
                <div className={styles.content}>
                    {children}
                </div>
            </div>
        </div>
    );
};
