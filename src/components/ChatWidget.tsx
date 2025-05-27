import React, { useState, useEffect, useRef } from 'react';
import '../styles/chat-widget.css';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

interface ChatWidgetProps {
  title?: string;
  subtitle?: string;
  placeholder?: string;
  welcomeMessage?: string;
  botName?: string;
  botAvatar?: string;
  userAvatar?: string;
  onSendMessage?: (message: string) => Promise<string>;
}

const ChatWidget: React.FC<ChatWidgetProps> = ({
  title = 'AIChat 상담',
  subtitle = '무엇을 도와드릴까요?',
  placeholder = '메시지를 입력하세요...',
  welcomeMessage = '안녕하세요! 무엇을 도와드릴까요?',
  botName = 'AI 상담사',
  botAvatar = '🤖',
  userAvatar = '👤',
  onSendMessage
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // 자동 스크롤
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 채팅창 열릴 때 환영 메시지
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const welcomeMsg: Message = {
        id: `welcome-${Date.now()}`,
        text: welcomeMessage,
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages([welcomeMsg]);
    }
  }, [isOpen, welcomeMessage]);

  // 메시지 전송 처리
  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    try {
      // 봇 응답 받기
      let botResponse = '죄송합니다. 잠시 후 다시 시도해주세요.';
      
      if (onSendMessage) {
        botResponse = await onSendMessage(inputValue);
      } else {
        // 기본 응답 로직
        await new Promise(resolve => setTimeout(resolve, 1000));
        botResponse = getBotResponse(inputValue);
      }

      const botMessage: Message = {
        id: `bot-${Date.now()}`,
        text: botResponse,
        sender: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('메시지 전송 오류:', error);
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        text: '오류가 발생했습니다. 다시 시도해주세요.',
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  // 기본 봇 응답 (실제로는 백엔드 API 호출)
  const getBotResponse = (userInput: string): string => {
    const input = userInput.toLowerCase();
    
    if (input.includes('예약')) {
      return '예약을 도와드리겠습니다. 원하시는 날짜와 시간을 알려주세요.';
    } else if (input.includes('가격') || input.includes('비용')) {
      return '시술별 가격 정보를 안내해드리겠습니다. 어떤 시술에 관심이 있으신가요?';
    } else if (input.includes('시술') || input.includes('추천')) {
      return '고객님의 피부 고민을 알려주시면 맞춤 시술을 추천해드릴게요.';
    } else if (input.includes('안녕')) {
      return '안녕하세요! 엘리트 뷰티 클리닉입니다. 무엇을 도와드릴까요?';
    } else {
      return '네, 고객님. 더 자세히 말씀해주시면 정확한 안내를 도와드리겠습니다.';
    }
  };

  // 엔터키 처리
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="chat-widget">
      {/* 플로팅 버튼 */}
      {!isOpen && (
        <button 
          className="chat-toggle-button"
          onClick={() => setIsOpen(true)}
          aria-label="채팅 열기"
        >
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12c0 1.54.36 3 .97 4.29L1 23l6.71-1.97C9 21.64 10.46 22 12 22c5.52 0 10-4.48 10-10S17.52 2 12 2zm0 18c-1.41 0-2.73-.36-3.88-.99l-.28-.15-2.94.77.79-2.87-.18-.3C4.9 15.3 4.5 13.68 4.5 12c0-4.41 3.59-8 8-8s8 3.59 8 8-3.59 8-8 8z"/>
            <path d="M7 11h2v2H7zm4 0h2v2h-2zm4 0h2v2h-2z"/>
          </svg>
        </button>
      )}

      {/* 채팅 창 */}
      {isOpen && (
        <div className="chat-window">
          {/* 헤더 */}
          <div className="chat-header">
            <h3>{title}</h3>
            <div className="chat-avatars">
              <div className="chat-avatar">{botAvatar}</div>
            </div>
            <p className="chat-subtitle">{subtitle}</p>
            <button
              className="chat-close"
              onClick={() => setIsOpen(false)}
              style={{
                position: 'absolute',
                top: '16px',
                right: '16px',
                background: 'none',
                border: 'none',
                color: 'var(--chat-text-secondary)',
                cursor: 'pointer',
                fontSize: '24px'
              }}
            >
              ×
            </button>
          </div>

          {/* 메시지 영역 */}
          <div className="chat-body">
            <div className="chat-messages">
              {messages.map(message => (
                <div
                  key={message.id}
                  className={`message message-${message.sender}`}
                >
                  {message.text}
                </div>
              ))}
              {isTyping && (
                <div className="message message-bot">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </div>

          {/* 입력 영역 */}
          <div className="chat-input-area">
            <div className="chat-input-wrapper">
              <input
                ref={inputRef}
                type="text"
                className="chat-input"
                placeholder={placeholder}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={isTyping}
              />
              <div className="chat-input-actions">
                <button 
                  className="chat-input-button"
                  onClick={handleSendMessage}
                  disabled={!inputValue.trim() || isTyping}
                >
                  <svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
                    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWidget;

// 타이핑 인디케이터 스타일 추가
const style = document.createElement('style');
style.textContent = `
  .typing-indicator {
    display: flex;
    align-items: center;
    gap: 4px;
  }
  
  .typing-indicator span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--chat-text-secondary);
    animation: typing 1.4s infinite ease-in-out;
  }
  
  .typing-indicator span:nth-child(1) {
    animation-delay: -0.32s;
  }
  
  .typing-indicator span:nth-child(2) {
    animation-delay: -0.16s;
  }
  
  @keyframes typing {
    0%, 80%, 100% {
      transform: scale(0.8);
      opacity: 0.5;
    }
    40% {
      transform: scale(1);
      opacity: 1;
    }
  }
  
  .chat-close {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
  }
  
  .chat-close:hover {
    background: var(--chat-secondary);
  }
  
  .chat-subtitle {
    margin: 0;
    font-size: 14px;
    color: var(--chat-text-secondary);
  }
`;
document.head.appendChild(style);
