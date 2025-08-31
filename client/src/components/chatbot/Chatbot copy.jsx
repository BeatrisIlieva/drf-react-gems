import { useRef, useState } from 'react';

import ReactMarkdown from 'react-markdown';

// Add this import
import { useChatbot } from '../../api/chatbotApi';

export const Chatbot = () => {
    const [message, setMessage] = useState('');
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [sessionId, setSessionId] = useState(null);

    const { sendMessage } = useChatbot();

    const assistantMessageRef = useRef('');

    const sendMessageHandler = async () => {
        if (!message.trim()) {
            setError('Please enter a message');
            return;
        }

        setLoading(true);
        setError('');

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
            sendMessage();
        }
    };

    return (
        <div
            style={{
                maxWidth: '800px',
                margin: '20px auto',
                padding: '20px',
                border: '1px solid #ddd',
                borderRadius: '8px',
                fontFamily: 'Arial, sans-serif',
            }}
        >
            <h2>Chatbot Test Interface</h2>

            {/* Session Info */}
            {sessionId && (
                <div
                    style={{
                        marginBottom: '10px',
                        padding: '8px',
                        backgroundColor: '#e8f5e8',
                        borderRadius: '4px',
                        fontSize: '12px',
                        color: '#2d5a2d',
                    }}
                >
                    Session ID: {sessionId}
                </div>
            )}

            {/* Error Display */}
            {error && (
                <div
                    style={{
                        backgroundColor: '#f8d7da',
                        color: '#721c24',
                        padding: '10px',
                        borderRadius: '4px',
                        marginBottom: '20px',
                        border: '1px solid #f5c6cb',
                    }}
                >
                    {error}
                </div>
            )}

            {/* Chat Messages */}
            <div
                style={{
                    height: '400px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    padding: '10px',
                    overflowY: 'auto',
                    marginBottom: '20px',
                    backgroundColor: '#f8f9fa',
                }}
            >
                {messages.length === 0 ? (
                    <p style={{ color: '#6c757d', fontStyle: 'italic' }}>
                        No messages yet. Start a conversation! Try saying "My name is [your name]"
                        and then ask about it in the next message.
                    </p>
                ) : (
                    messages.map((msg, index) => (
                        <div
                            key={index}
                            style={{
                                marginBottom: '10px',
                                padding: '8px',
                                borderRadius: '4px',
                                backgroundColor:
                                    msg.role === 'user'
                                        ? '#e3f2fd'
                                        : msg.role === 'error'
                                          ? '#ffebee'
                                          : '#f3e5f5',
                                borderLeft: `4px solid ${
                                    msg.role === 'user'
                                        ? '#2196f3'
                                        : msg.role === 'error'
                                          ? '#f44336'
                                          : '#9c27b0'
                                }`,
                            }}
                        >
                            <div
                                style={{
                                    fontSize: '12px',
                                    color: '#666',
                                    marginBottom: '4px',
                                    fontWeight: 'bold',
                                }}
                            >
                                {msg.role === 'user'
                                    ? 'You'
                                    : msg.role === 'error'
                                      ? 'Error'
                                      : 'Assistant'}{' '}
                                - {msg.timestamp}
                            </div>
                            <div>
                                {msg.role === 'assistant' ? (
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
                                        {msg.content ||
                                            (loading && msg.role === 'assistant'
                                                ? 'Thinking...'
                                                : '')}
                                    </ReactMarkdown>
                                ) : (
                                    <div style={{ whiteSpace: 'pre-wrap' }}>
                                        {msg.content ||
                                            (loading && msg.role === 'assistant'
                                                ? 'Thinking...'
                                                : '')}
                                    </div>
                                )}
                            </div>
                        </div>
                    ))
                )}
            </div>

            {/* Input Section */}
            <div style={{ display: 'flex', gap: '10px' }}>
                <textarea
                    value={message}
                    onChange={e => setMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Type your message here... (Press Enter to send)"
                    style={{
                        flex: 1,
                        padding: '10px',
                        border: '1px solid #ddd',
                        borderRadius: '4px',
                        resize: 'vertical',
                        minHeight: '60px',
                        fontSize: '14px',
                    }}
                    disabled={loading}
                />
                <button
                    onClick={sendMessageHandler}
                    disabled={loading || !message.trim()}
                    style={{
                        padding: '10px 20px',
                        backgroundColor: loading ? '#ccc' : '#28a745',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: loading ? 'not-allowed' : 'pointer',
                        fontSize: '14px',
                        minWidth: '80px',
                    }}
                >
                    {loading ? 'Sending...' : 'Send'}
                </button>
            </div>
        </div>
    );
};
