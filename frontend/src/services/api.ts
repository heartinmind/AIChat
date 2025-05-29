import axios from 'axios';
import { 
  RouteResponse, 
  UserCreateRequest, 
  SessionCreateRequest,
  MessageCreateRequest,
  ClinicInfo 
} from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

console.log('API Base URL:', API_BASE_URL);

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor with logging
apiClient.interceptors.request.use(
  (config) => {
    console.log('API Request:', {
      method: config.method,
      url: config.url,
      data: config.data,
      headers: config.headers
    });
    
    // 토큰이 있다면 추가
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor with logging
apiClient.interceptors.response.use(
  (response) => {
    console.log('API Response:', {
      status: response.status,
      data: response.data,
      url: response.config.url
    });
    return response;
  },
  (error) => {
    console.error('API Error:', {
      status: error.response?.status,
      data: error.response?.data,
      url: error.config?.url,
      message: error.message
    });
    
    if (error.response?.status === 401) {
      // 인증 오류 처리
      localStorage.removeItem('auth_token');
    }
    return Promise.reject(error);
  }
);

export const chatApi = {
  // 라우팅 확인 (AI or 상담원)
  checkRoute: async (): Promise<RouteResponse> => {
    const response = await apiClient.post('/api/session/route');
    return response.data;
  },

  // 사용자 생성/조회
  createUser: async (userData: UserCreateRequest) => {
    const requestData = {
      name: userData.name,
      phone: userData.phone,
      gender: userData.gender,
      birth_year: userData.birthYear,
    };
    console.log('Creating user with data:', requestData);
    const response = await apiClient.post('/api/users', requestData);
    return response.data;
  },

  // 세션 생성
  createSession: async (sessionData: SessionCreateRequest) => {
    console.log('Creating session with data:', sessionData);
    const response = await apiClient.post('/api/sessions', sessionData);
    return response.data;
  },

  // 메시지 전송
  sendMessage: async (messageData: MessageCreateRequest) => {
    console.log('Sending message with data:', messageData);
    const response = await apiClient.post('/api/messages', messageData);
    return response.data;
  },

  // 세션 메시지 조회
  getSessionMessages: async (sessionId: string) => {
    const response = await apiClient.get(`/api/sessions/${sessionId}/messages`);
    return response.data;
  },

  // 세션 종료
  endSession: async (sessionId: string) => {
    const response = await apiClient.put(`/api/sessions/${sessionId}/end`);
    return response.data;
  },

  // 병원 정보 조회
  getClinicInfo: async (category?: string): Promise<ClinicInfo[]> => {
    const response = await apiClient.get('/api/clinic/info', {
      params: { category },
    });
    return response.data;
  },
};

// 상담원 API (별도)
export const agentApi = {
  // 상담원 로그인
  login: async (email: string, password: string) => {
    const response = await apiClient.post('/api/agents/login', {
      email,
      password,
    });
    return response.data;
  },

  // 상담원 세션 목록
  getAgentSessions: async () => {
    const response = await apiClient.get('/api/agents/sessions');
    return response.data;
  },
};