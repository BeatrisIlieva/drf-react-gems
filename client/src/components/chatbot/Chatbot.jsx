import { useEffect, useRef, useState } from 'react';

import { Button } from '../reusable/button/Button';
import { Icon } from '../reusable/icon/Icon';
import ReactMarkdown from 'react-markdown';

// Add this import
import { useChatbot } from '../../api/chatbotApi';

import styles from './Chatbot.module.scss';

export const Chatbot = () => {
    const [message, setMessage] = useState('');
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [sessionId, setSessionId] = useState(null);

    const { sendMessage } = useChatbot();

    const assistantMessageRef = useRef('');
    // Add ref for messages container
    const messagesEndRef = useRef(null);

    // Add auto-scroll function
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    // Add useEffect to scroll when messages change
    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const startConversationHandler = () => {
        const pendingAiMessage = {
            role: 'assistant',
            content:
                "Hi, I'm the DRF React Gems Virtual Jewelry Consultant. Every piece of jewelry tells a story. What special moment or occasion brings you to DRF React Gems today?",
            timestamp: new Date().toLocaleTimeString(),
        };
        setMessages(prev => [...prev, pendingAiMessage]);
    };

    const sendMessageHandler = async () => {
        if (!message.trim()) {
            setError('Please enter a message');
            return;
        }

        setLoading(true);
        setError('');
        setMessage('');

        // Add user message to chat
        const userMessage = {
            role: 'user',
            content: message,
            timestamp: new Date().toLocaleTimeString(),
        };
        setMessages(prev => [...prev, userMessage]);

        // Start a pending assistant message
        const pendingAiMessage = {
            role: 'assistant',
            content: '',
            timestamp: new Date().toLocaleTimeString(),
        };
        setMessages(prev => [...prev, pendingAiMessage]);

        assistantMessageRef.current = '';

        try {
            // Prepare request payload
            const payload = {
                message: message,
            };

            // Add session_id if we have one
            if (sessionId) {
                payload.session_id = sessionId;
            }

            const response = await sendMessage(payload);

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });

                // Process complete lines (SSE events are \n\n separated)
                let lines;
                while ((lines = buffer.split('\n\n')).length > 1) {
                    const event = lines.shift().trim();
                    buffer = lines.join('\n\n');

                    // Parse 'data:' lines
                    if (event.startsWith('data:')) {
                        const dataStr = event.slice(5).trim();
                        let data;
                        try {
                            data = JSON.parse(dataStr);
                        } catch (parseErr) {
                            console.error('Invalid JSON in SSE:', parseErr);
                            continue;
                        }

                        // Handle session_id
                        if (data.session_id && !sessionId) {
                            setSessionId(data.session_id);
                            console.log('Session ID set:', data.session_id);
                        }

                        if (data.chunk === '[DONE]') {
                            // Streaming complete
                            break;
                        } else if (data.error) {
                            // Handle error chunk
                            setError(data.error);
                            setMessages(prev => {
                                const updated = [...prev];
                                const last = updated[updated.length - 1];
                                last.content += `\nError: ${data.error}`;
                                last.role = 'error';
                                return updated;
                            });
                            break;
                        } else if (data.chunk) {
                            assistantMessageRef.current += data.chunk;

                            setMessages(prev => {
                                const updated = [...prev];
                                const last = { ...updated[updated.length - 1] };
                                last.content = assistantMessageRef.current;
                                updated[updated.length - 1] = last;
                                return updated;
                            });
                        }
                    }
                }
            }
        } catch (error) {
            const errorMsg = error.message;

            setError(errorMsg);
            setMessages(prev => {
                const updated = [...prev];
                const last = { ...updated[updated.length - 1] };
                last.content = `Error: ${errorMsg}`;
                last.role = 'error';
                updated[updated.length - 1] = last;
                return updated;
            });
        }

        setMessage('');
        setLoading(false);
    };

    const handleKeyPress = e => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessageHandler();
        }
    };

    return (
        <div className={styles['chatbot']}>
            <div className={styles['header']}>What with an Advisor</div>
            {messages.length > 0 ? (
                <>
                    <div className={styles['messages']}>
                        <div className={styles['time-wrapper']}>
                            <span>Today</span>
                            <span></span>
                            {messages[0].timestamp}
                        </div>
                        <div className={styles['wrapper']}>
                            {messages.map((msg, index) => (
                                <>
                                    {msg.role === 'user' ? (
                                        <div key={index}>
                                            <span className={styles['message-content']}>
                                                {msg.content}
                                            </span>
                                            <span className={styles['time-span']}>{msg.timestamp}</span>
                                        </div>
                                    ) : (
                                        <div key={index}>
                                            <div className={styles['thumbnail']}>
                                                <img src="/logo.webp" alt="logo" />
                                            </div>
                                            <div className={styles['message-content']}>
                                                <ReactMarkdown
                                                    components={{
                                                        img: ({ node, ...props }) => (
                                                            <img
                                                                {...props}
                                                                style={{
                                                                    maxWidth: '100%',
                                                                    height: 'auto',
                                                                    borderRadius: '4px',
                                                                    margin: '10px 0',
                                                                }}
                                                            />
                                                        ),
                                                        a: ({ node, ...props }) => (
                                                            <a
                                                                {...props}
                                                                style={{
                                                                    color: '#007bff',
                                                                    textDecoration: 'none',
                                                                }}
                                                                rel="noopener noreferrer"
                                                            >
                                                                {props.children}
                                                            </a>
                                                        ),
                                                    }}
                                                >
                                                    {msg.content || (loading ? 'Thinking...' : '')}
                                                </ReactMarkdown>
                                            </div>
                                            <span className={styles['time-span']}>DRf React Gems Virtual Jewelry Consultant {msg.timestamp}</span>
                                        </div>
                                    )}
                                </>
                            ))}
                            {/* Add invisible div for scroll target */}
                            <div className={styles['ref-div']} ref={messagesEndRef} />
                        </div>
                    </div>
                    <div className={styles['text-area']}>
                        <textarea
                            value={message}
                            onChange={e => setMessage(e.target.value)}
                            onKeyDown={handleKeyPress}
                            placeholder={
                                loading ? 'Waiting for response...' : 'Type your message...'
                            }
                            disabled={loading}
                        ></textarea>
                        <span
                            className={
                                message
                                    ? `${styles['send-button']} ${styles['visible']}`
                                    : `${styles['send-button']}`
                            }
                        >
                            <Icon name="send" />
                        </span>
                    </div>
                </>
            ) : (
                <div className={styles['no-messages-yet']}>
                    <h4>HOW CAN WE HELP?</h4>
                    <p>Our Virtual Jewelry Consultant is ready to assist you.</p>

                    <p>
                        Note that artificial intelligence is a developing technology and this
                        chatbot may make mistakes or provide inaccurate information.
                    </p>

                    <Button
                        title="Chat Now"
                        callbackHandler={startConversationHandler}
                        color="black"
                    />
                </div>
            )}
        </div>
    );
};
