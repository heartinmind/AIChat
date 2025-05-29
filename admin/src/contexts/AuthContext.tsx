import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://elite-beauty-api-225954711662.asia-northeast3.run.app';

interface Agent {
  agent_id: string;
  email: string;
  name: string;
  is_admin: boolean;
}

interface AuthContextType {
  agent: Agent | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Axios 인스턴스 생성
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - 토큰 자동 추가
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [agent, setAgent] = useState<Agent | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const isAuthenticated = !!token && !!agent;

  // 토큰 디코드 및 에이전트 정보 설정
  const decodeAndSetAgent = (token: string) => {
    try {
      const decoded: any = jwtDecode(token);
      setAgent({
        agent_id: decoded.agent_id,
        email: decoded.email,
        name: decoded.name || decoded.email,
        is_admin: decoded.is_admin,
      });
      return true;
    } catch (err) {
      console.error('토큰 디코드 실패:', err);
      return false;
    }
  };

  // 로그인
  const login = useCallback(async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await api.post('/api/agents/login', { email, password });
      const { access_token, agent_id, is_admin } = response.data;

      // 토큰 저장
      localStorage.setItem('token', access_token);
      setToken(access_token);

      // 에이전트 정보 설정
      if (decodeAndSetAgent(access_token)) {
        // 관리자가 아닌 경우 에러
        if (!is_admin) {
          throw new Error('관리자 권한이 필요합니다.');
        }
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || '로그인 실패';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // 로그아웃
  const logout = useCallback(() => {
    localStorage.removeItem('token');
    setToken(null);
    setAgent(null);
  }, []);

  // 인증 확인
  const checkAuth = useCallback(async () => {
    const savedToken = localStorage.getItem('token');
    
    if (!savedToken) {
      setIsLoading(false);
      return;
    }

    // 토큰 유효성 검증
    if (decodeAndSetAgent(savedToken)) {
      setToken(savedToken);
      
      // 서버에 토큰 유효성 확인 (선택적)
      try {
        await api.get('/api/admin/dashboard');
      } catch (err) {
        // 토큰이 유효하지 않으면 로그아웃
        logout();
      }
    } else {
      logout();
    }
    
    setIsLoading(false);
  }, [logout]);

  // 초기 인증 확인
  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const contextValue: AuthContextType = {
    agent,
    token,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    checkAuth,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

// API 인스턴스 export (다른 컴포넌트에서 사용)
export { api };
