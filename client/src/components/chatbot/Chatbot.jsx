import { useEffect, useRef, useState } from 'react';

import { Link } from 'react-router';

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
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isTextShown, setIsTextShown] = useState(false);
    const { sendMessage } = useChatbot();

    const assistantMessageRef = useRef('');
    // Add ref for messages container
    const messagesEndRef = useRef(null);
    // Add ref for textarea
    const textareaRef = useRef(null);

    // Add auto-scroll function
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    // Add useEffect to scroll when messages change
    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Add useEffect to auto-focus textarea when loading completes
    useEffect(() => {
        if (!loading && textareaRef.current) {
            textareaRef.current.focus();
        }
    }, [loading]);

    const renderThinkingText = text => {
        return (
            <span className={styles['thinking-text']}>
                {text.split('').map((char, index) => (
                    <span
                        key={index}
                        className={styles['thinking-char']}
                        style={{
                            animationDelay: `${index * 0.1}s`,
                        }}
                    >
                        {char === ' ' ? '\u00A0' : char}
                    </span>
                ))}
            </span>
        );
    };

    const getTimestamp = () => {
        const time = new Date().toLocaleString('en-US', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true,
        });
        return time.replace(/(am|pm)$/i, match => match.toUpperCase());
    };

    const startConversationHandler = () => {
        const pendingAiMessage = {
            role: 'assistant',
            content:
                "Hi, I'm the DRF React Gems Virtual Jewelry Consultant. Every piece of jewelry tells a story. What special moment or occasion brings you to DRF React Gems today?",
            timestamp: getTimestamp(),
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
            timestamp: getTimestamp(),
        };
        setMessages(prev => [...prev, userMessage]);

        // Start a pending assistant message WITHOUT timestamp
        const pendingAiMessage = {
            role: 'assistant',
            content: '',
            timestamp: null, // Don't set timestamp until response is complete
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
                if (done) {
                    console.log('Stream ended, checking if timestamp is set');
                    // Fallback: set timestamp if streaming ends and no timestamp was set
                    setMessages(prev => {
                        const updated = [...prev];
                        const lastMessage = updated[updated.length - 1];
                        if (!lastMessage.timestamp && lastMessage.role === 'assistant') {
                            console.log('Setting fallback timestamp');
                            updated[updated.length - 1] = {
                                ...lastMessage,
                                timestamp: getTimestamp(),
                            };
                        }
                        return updated;
                    });
                    break;
                }

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
                        }

                        if (data.chunk === '[DONE]') {
                            console.log('DONE received, setting timestamp');
                            // Set timestamp when response is complete
                            setMessages(prev => {
                                const updated = [...prev];
                                updated[updated.length - 1] = {
                                    ...updated[updated.length - 1],
                                    timestamp: getTimestamp(),
                                };
                                console.log(
                                    'Updated message with timestamp:',
                                    updated[updated.length - 1]
                                );
                                return updated;
                            });
                            // Streaming complete
                            break;
                        } else if (data.error) {
                            // Handle error chunk - set timestamp for error too
                            setError(data.error);
                            setMessages(prev => {
                                const updated = [...prev];
                                updated[updated.length - 1] = {
                                    ...updated[updated.length - 1],
                                    content:
                                        updated[updated.length - 1].content + `\n${data.error}`,
                                    role: 'error',
                                    timestamp: getTimestamp(),
                                };
                                return updated;
                            });
                            break;
                        } else if (data.chunk) {
                            assistantMessageRef.current += data.chunk;

                            setMessages(prev => {
                                const updated = [...prev];
                                updated[updated.length - 1] = {
                                    ...updated[updated.length - 1],
                                    content: assistantMessageRef.current,
                                };
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
                updated[updated.length - 1] = {
                    ...updated[updated.length - 1],
                    content: `Error: ${errorMsg}`,
                    role: 'error',
                    timestamp: getTimestamp(),
                };
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
        <>
            {!isModalOpen && (
                <span
                    className={styles['open-modal']}
                    onMouseEnter={() => setIsTextShown(true)}
                    onMouseLeave={() => setIsTextShown(false)}
                >
                    {isTextShown ? (
                        <span
                            className={styles['chat-with-a-consultant']}
                            onClick={() => {
                                setIsModalOpen(true);
                                setIsTextShown(false);
                            }}
                        >
                            {messages.length > 0 ? 'Resume Chat' : 'Chat With A jewelry Consultant'}
                        </span>
                    ) : (
                        <Icon name="chat" color="white" />
                    )}
                </span>
            )}
            {isModalOpen && (
                <div className={styles['chatbot']}>
                    <div className={styles['header']}>
                        <span>Chat with a Jewelry Consultant</span>
                        <Icon name="minimize" callbackHandler={() => setIsModalOpen(false)} />
                    </div>
                    {messages.length > 0 ? (
                        <>
                            <div className={styles['messages']}>
                                <div className={styles['time-wrapper']}>
                                    <span>Today</span>
                                    <span className={styles['time-separator']}></span>
                                    {messages[0].timestamp}
                                </div>
                                <div className={styles['welcome-wrapper']}>
                                    <span className={styles['inner-wrapper']}>
                                        <span>
                                            DRF React Gems Jewelry Consultant has joined the chat
                                        </span>
                                        <span>{messages[0].timestamp}</span>
                                    </span>
                                </div>
                                <div className={styles['wrapper']}>
                                    {messages.map((msg, index) => (
                                        <>
                                            {msg.role === 'user' ? (
                                                <div key={index}>
                                                    <span className={styles['message-content']}>
                                                        {msg.content}
                                                    </span>
                                                    <span className={styles['time-span']}>
                                                        {msg.timestamp}
                                                    </span>
                                                </div>
                                            ) : (
                                                <div key={index}>
                                                    <div className={styles['thumbnail']}>
                                                        <img src="/logo.webp" alt="logo" />
                                                    </div>
                                                    <div className={styles['message-content']}>
                                                        {msg.content ? (
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
                                                                    a: ({
                                                                        href,
                                                                        children,
                                                                        ...props
                                                                    }) => {
                                                                        // Internal link
                                                                        if (
                                                                            href.startsWith(
                                                                                '/products'
                                                                            )
                                                                        ) {
                                                                            return (
                                                                                <Link
                                                                                    to={href}
                                                                                    {...props}
                                                                                >
                                                                                    {children}
                                                                                </Link>
                                                                            );
                                                                        }

                                                                        // External link
                                                                        return (
                                                                            <a
                                                                                href={href}
                                                                                target="_blank"
                                                                                rel="noopener noreferrer"
                                                                                {...props}
                                                                            >
                                                                                {children}
                                                                            </a>
                                                                        );
                                                                    },
                                                                }}
                                                            >
                                                                {msg.content}
                                                            </ReactMarkdown>
                                                        ) : (
                                                            loading &&
                                                            renderThinkingText('Thinking...')
                                                        )}
                                                    </div>
                                                    <span className={styles['time-span']}>
                                                        <span>Virtual Jewelry Consultant</span>
                                                        {msg.timestamp && (
                                                            <>
                                                                <span
                                                                    className={
                                                                        styles['time-separator']
                                                                    }
                                                                ></span>
                                                                {msg.timestamp}
                                                            </>
                                                        )}
                                                    </span>
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
                                    ref={textareaRef}
                                    value={message}
                                    autoFocus
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
                                    <Icon name="send" callbackHandler={sendMessageHandler} />
                                </span>
                            </div>
                        </>
                    ) : (
                        <div className={styles['no-messages-yet']}>
                            <h4>HOW CAN WE HELP?</h4>
                            <p>Our Virtual Jewelry Consultant is ready to assist you.</p>
                            <p>
                                For best experience, please provide detailed questions and clear
                                responses. This helps our consultant understand your specific needs
                                better.
                            </p>

                            <Button
                                title="Chat Now"
                                callbackHandler={startConversationHandler}
                                color="black"
                            />
                        </div>
                    )}
                </div>
            )}
        </>
    );
};
