import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const Chatbot = ({ currentProject, onClose }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [isMinimized, setIsMinimized] = useState(false);
  const messagesEndRef = useRef(null);

  // Load suggestions and initial message
  useEffect(() => {
    loadSuggestions();
    setMessages([
      {
        id: 1,
        text: "Hello! I'm ScopeAI Assistant. I specialize in project scoping and planning. How can I help you with your project today?",
        isBot: true,
        timestamp: new Date()
      }
    ]);
  }, []);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadSuggestions = async () => {
    try {
      const response = await axios.get('/api/chatbot/suggestions');
      setSuggestions(response.data.suggestions);
    } catch (error) {
      console.error('Error loading suggestions:', error);
      // Fallback suggestions
      setSuggestions([
        "How do I estimate project timeline?",
        "What should be included in project scope?",
        "How to create a resource plan?",
        "What are common cost estimation techniques?"
      ]);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const sendMessage = async (message = inputMessage) => {
    if (!message.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: message,
      isBot: false,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post('/api/chatbot/chat', {
        message: message,
        project_id: currentProject?.id
      });

      const botMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        isBot: true,
        isScopeRelated: response.data.is_scope_related,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: "I'm here to help with project scoping! For the best experience, make sure the backend server is running. Meanwhile, I can help you with:\n\n• Project timeline estimation\n• Resource planning\n• Cost estimation techniques\n• Scope definition",
        isBot: true,
        isError: true,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage();
  };

  const handleSuggestionClick = (suggestion) => {
    sendMessage(suggestion);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  if (isMinimized) {
    return (
      <div style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        width: '300px',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        borderRadius: '12px',
        boxShadow: '0 8px 25px rgba(0,0,0,0.15)',
        zIndex: 1000,
        cursor: 'pointer'
      }} onClick={() => setIsMinimized(false)}>
        <div style={{
          padding: '15px',
          color: 'white',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              background: '#4CAF50'
            }}></div>
            <span style={{ fontWeight: '600' }}>ScopeAI Assistant</span>
          </div>
          <div style={{ fontSize: '12px', opacity: 0.8 }}>
            Click to open
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      width: '400px',
      height: '500px',
      background: 'white',
      borderRadius: '12px',
      boxShadow: '0 10px 30px rgba(0,0,0,0.2)',
      display: 'flex',
      flexDirection: 'column',
      zIndex: 1000,
      overflow: 'hidden'
    }}>
      {/* Header */}
      <div style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        padding: '15px 20px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            background: '#4CAF50'
          }}></div>
          <div>
            <div style={{ fontWeight: '600', fontSize: '16px' }}>ScopeAI Assistant</div>
            <div style={{ fontSize: '12px', opacity: 0.8 }}>
              {currentProject ? `Helping with: ${currentProject.name}` : 'Project Scoping Expert'}
            </div>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            onClick={() => setIsMinimized(true)}
            style={{
              background: 'none',
              border: 'none',
              color: 'white',
              cursor: 'pointer',
              fontSize: '16px',
              opacity: 0.8
            }}
          >
            −
          </button>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              color: 'white',
              cursor: 'pointer',
              fontSize: '16px',
              opacity: 0.8
            }}
          >
            ×
          </button>
        </div>
      </div>

      {/* Messages */}
      <div style={{
        flex: 1,
        padding: '15px',
        overflowY: 'auto',
        background: '#f8f9fa'
      }}>
        {messages.map((message) => (
          <div
            key={message.id}
            style={{
              display: 'flex',
              justifyContent: message.isBot ? 'flex-start' : 'flex-end',
              marginBottom: '12px'
            }}
          >
            <div style={{
              maxWidth: '85%',
              background: message.isBot ? 'white' : '#667eea',
              color: message.isBot ? '#333' : 'white',
              padding: '10px 14px',
              borderRadius: message.isBot ? '12px 12px 12px 4px' : '12px 12px 4px 12px',
              boxShadow: '0 2px 6px rgba(0,0,0,0.1)',
              lineHeight: '1.4'
            }}>
              <div style={{ whiteSpace: 'pre-wrap' }}>
                {message.text}
              </div>
              <div style={{
                fontSize: '10px',
                opacity: 0.6,
                marginTop: '4px',
                textAlign: 'right'
              }}>
                {formatTime(message.timestamp)}
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div style={{ display: 'flex', justifyContent: 'flex-start', marginBottom: '12px' }}>
            <div style={{
              background: 'white',
              padding: '10px 14px',
              borderRadius: '12px 12px 12px 4px',
              boxShadow: '0 2px 6px rgba(0,0,0,0.1)',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}>
              <div style={{ display: 'flex', gap: '3px' }}>
                <div style={{
                  width: '6px',
                  height: '6px',
                  borderRadius: '50%',
                  background: '#667eea',
                  animation: 'bounce 1.4s infinite ease-in-out'
                }}></div>
                <div style={{
                  width: '6px',
                  height: '6px',
                  borderRadius: '50%',
                  background: '#667eea',
                  animation: 'bounce 1.4s infinite ease-in-out',
                  animationDelay: '0.1s'
                }}></div>
                <div style={{
                  width: '6px',
                  height: '6px',
                  borderRadius: '50%',
                  background: '#667eea',
                  animation: 'bounce 1.4s infinite ease-in-out',
                  animationDelay: '0.2s'
                }}></div>
              </div>
              <span style={{ fontSize: '13px', color: '#666' }}>Thinking...</span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Suggestions */}
      {suggestions.length > 0 && messages.length <= 2 && (
        <div style={{
          padding: '12px 15px',
          background: '#f1f3f4',
          borderTop: '1px solid #e1e5e9'
        }}>
          <div style={{ fontSize: '11px', color: '#666', marginBottom: '6px', fontWeight: '600' }}>
            QUICK QUESTIONS:
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
            {suggestions.slice(0, 3).map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(suggestion)}
                style={{
                  background: 'white',
                  border: '1px solid #e1e5e9',
                  borderRadius: '16px',
                  padding: '4px 10px',
                  fontSize: '11px',
                  cursor: 'pointer',
                  color: '#667eea',
                  transition: 'all 0.2s'
                }}
                onMouseEnter={(e) => {
                  e.target.style.background = '#667eea';
                  e.target.style.color = 'white';
                }}
                onMouseLeave={(e) => {
                  e.target.style.background = 'white';
                  e.target.style.color = '#667eea';
                }}
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <form onSubmit={handleSubmit} style={{
        padding: '12px 15px',
        borderTop: '1px solid #e1e5e9',
        background: 'white'
      }}>
        <div style={{ display: 'flex', gap: '8px' }}>
          <input
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about project scoping..."
            style={{
              flex: 1,
              padding: '10px 12px',
              border: '1px solid #e1e5e9',
              borderRadius: '6px',
              fontSize: '13px'
            }}
          />
          <button
            type="submit"
            disabled={!inputMessage.trim() || isLoading}
            style={{
              background: inputMessage.trim() ? '#667eea' : '#ccc',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              padding: '10px 14px',
              cursor: inputMessage.trim() ? 'pointer' : 'not-allowed',
              fontSize: '13px'
            }}
          >
            Send
          </button>
        </div>
      </form>

      <style jsx>{`
        @keyframes bounce {
          0%, 80%, 100% {
            transform: scale(0);
          }
          40% {
            transform: scale(1);
          }
        }
      `}</style>
    </div>
  );
};

export default Chatbot;
