import { useCallback } from 'react';

import { HOST } from '../constants/host';

const baseUrl = `${HOST}/api/chatbot/chat/`;

export const useChatbot = () => {
    const sendMessage = useCallback(async data => {
        try {
            const response = await fetch(`${baseUrl}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            return response;
        } catch (error) {
            console.error(error);
        }
    }, []);

    return {
        sendMessage,
    };
};
