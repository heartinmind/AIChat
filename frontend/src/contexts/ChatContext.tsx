import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import axios from 'axios';
import io, { Socket } from 'socket.io-client';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface User {
  user_id: string;
  name: string;
  phone: string;
  is_existing: boolean;
}

interface Session {
  session_id: string;
  is_new: boolean;
  route_target: 'ai' | 'agent';
}

interface Message {
  message_id: string;
  sender: 'user' | 'agent' | 'ai';
  content: string;
  timestamp: string;
  emotion_tag?: string;
}

interface ChatContextType {
  user: User | null;
  session: Session | null;
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  socket: Socket | null;
  
  // Actions
  createUser: (name: string, phone: string) => Promise<void>;
  createSession: () => Promise<void>;
  sendMessage: (content: string) => Promise<void>;
  endSession: () => Promise<void>;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [socket, setSocket] = useState<Socket | null>(null);

  // API 클라이언트 설정
  const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // 사용자 생성
  const createUser = useCallback(async (name: string, phone: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await api.post('/api/users', { name, phone });
      setUser(response.data);
      
      // 사용자 정보 로컬 스토리지에 저장
      localStorage.setItem('user', JSON.stringify(response.data));
    } catch (err: any) {
      setError(err.response?.data?.detail || '사용자 생성 중 오류가 발생했습니다.');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [api]);

  // 세션 생성
  const createSession = useCallback(async () => {
    if (!user) {
      setError('사용자 정보가 없습니다.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // 먼저 라우팅 확인 (AI or 상담원)
      const routeResponse = await api.post('/api/session/route');
      const routeTarget = routeResponse.data.target;
      
      // 세션 생성
      const response = await api.post('/api/sessions', {
        user_id: user.user_id,
        route_target: routeTarget,
      });
      
      setSession({
        ...response.data,
        route_target: routeTarget
      });
      
      // WebSocket 연결 (실시간 채팅용)
      if (response.data.route_target === 'agent') {
        const newSocket = io(API_BASE_URL, {
          path: '/ws',
          query: { session_id: response.data.session_id },
        });
        
        newSocket.on('message', (msg: Message) => {
          setMessages(prev => [...prev, msg]);
        });
        
        setSocket(newSocket);
      }
      
      // 기존 메시지 로드
      if (!response.data.is_new) {
        const messagesResponse = await api.get(`/api/sessions/${response.data.session_id}/messages`);
        setMessages(messagesResponse.data);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || '세션 생성 중 오류가 발생했습니다.');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [user, api]);

  // 메시지 전송
  const sendMessage = useCallback(async (content: string) => {
    if (!session) {
      setError('세션이 없습니다.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // 즉시 사용자 메시지 추가 (낙관적 업데이트)
      const userMessage: Message = {
        message_id: `temp-${Date.now()}`,
        sender: 'user',
        content,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, userMessage]);

      // API 호출
      const response = await api.post('/api/messages', {
        session_id: session.session_id,
        content,
      });

      // AI/상담원 응답 처리
      if (response.data.response) {
        const responseMessage: Message = {
          message_id: `resp-${Date.now()}`,
          sender: response.data.sender as 'ai' | 'agent',
          content: response.data.response,
          timestamp: new Date().toISOString(),
        };
        setMessages(prev => [...prev, responseMessage]);
      }

    } catch (err: any) {
      setError(err.response?.data?.detail || '메시지 전송 중 오류가 발생했습니다.');
      // 낙관적 업데이트 롤백
      setMessages(prev => prev.filter(msg => !msg.message_id.startsWith('temp-')));
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [session, api]);

  // 세션 종료
  const endSession = useCallback(async () => {
    if (!session) return;

    try {
      await api.post(`/api/sessions/${session.session_id}/end`);
      
      // WebSocket 연결 해제
      if (socket) {
        socket.disconnect();
        setSocket(null);
      }
      
      // 상태 초기화
      setSession(null);
      setMessages([]);
      
    } catch (err: any) {
      setError(err.response?.data?.detail || '세션 종료 중 오류가 발생했습니다.');
    }
  }, [session, socket, api]);

  // 컴포넌트 마운트 시 저장된 사용자 정보 복원
  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  // 컴포넌트 언마운트 시 정리
  useEffect(() => {
    return () => {
      if (socket) {
        socket.disconnect();
      }
    };
  }, [socket]);

  const contextValue: ChatContextType = {
    user,
    session,
    messages,
    isLoading,
    error,
    socket,
    createUser,
    createSession,
    sendMessage,
    endSession,
  };

  return (
    <ChatContext.Provider value={contextValue}>
      {children}
    </ChatContext.Provider>
  );
};
