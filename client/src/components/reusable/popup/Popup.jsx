import { useEffect, useRef } from 'react';

import { Icon } from '../icon/Icon';
import { createPortal } from 'react-dom';

import styles from './Popup.module.scss';

export const Popup = ({ isOpen, onClose, children }) => {
    const popupRef = useRef(null);
    const overlayRef = useRef(null);

    useEffect(() => {
        const handleEscapeKey = event => {
            if (event.key === 'Escape') {
                onClose();
            }
        };

        const handleClickOutside = event => {
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

    return createPortal(
        <div className={styles['overlay']} ref={overlayRef}>
            <div className={styles['popup']} ref={popupRef}>
                <button
                    className={styles['close-button']}
                    onClick={onClose}
                    aria-label="Close popup"
                >
                    <Icon name="xMark" fontSize={0.9} />
                </button>
                <div className={styles['content']}>{children}</div>
            </div>
        </div>,
        document.body
    );
};
