import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { Message, User, Session, UserCreateRequest } from '@/types';
import { chatApi } from '@/services/api';
import { v4 as uuidv4 } from 'uuid';

interface ChatState {
  user: User | null;
  session: Session | null;
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  
  // Actions
  initializeChat: (userData: UserCreateRequest) => Promise<void>;
  sendMessage: (content: string) => Promise<void>;
  endSession: () => Promise<void>;
  reset: () => void;
}

export const useChatStore = create<ChatState>()(
  devtools(
    (set, get) => ({
      user: null,
      session: null,
      messages: [],
      isLoading: false,
      error: null,

      initializeChat: async (userData: UserCreateRequest) => {
        set({ isLoading: true, error: null });
        
        try {
          // 1. 라우팅 확인 (AI or 상담원)
          const routeResponse = await chatApi.checkRoute();
          
          // 2. 사용자 생성/조회
          const userResponse = await chatApi.createUser(userData);
          
          // 3. 세션 생성
          const sessionResponse = await chatApi.createSession({
            user_id: userResponse.user_id,
            route_target: routeResponse.target,
          });
          
          set({
            user: {
              user_id: userResponse.user_id,
              name: userData.name,
              phone: userData.phone,
              gender: userData.gender,
              birth_year: userData.birthYear,
            },
            session: {
              session_id: sessionResponse.session_id,
              user_id: userResponse.user_id,
              started_at: new Date().toISOString(),
              status: 'active',
              source: 'web',
              route_target: routeResponse.target,
            },
            isLoading: false,
          });
          
          // 환영 메시지 추가
          const welcomeMessage: Message = {
            id: uuidv4(),
            session_id: sessionResponse.session_id,
            sender: 'system',
            content: `안녕하세요 ${userData.name}님! 엘리트 뷰티 클리닉입니다. ${
              routeResponse.target === 'ai' 
                ? 'AI 상담사가 도와드리겠습니다.' 
                : '잠시만 기다려주시면 상담원이 연결됩니다.'
            }`,
            timestamp: new Date().toISOString(),
          };
          
          set((state) => ({
            messages: [...state.messages, welcomeMessage],
          }));
          
        } catch (error: any) {
          set({ 
            error: error.message || '초기화 중 오류가 발생했습니다.',
            isLoading: false,
          });
          throw error;
        }
      },

      sendMessage: async (content: string) => {
        const { session, messages } = get();
        
        if (!session) {
          throw new Error('세션이 초기화되지 않았습니다.');
        }
        
        // 사용자 메시지 추가
        const userMessage: Message = {
          id: uuidv4(),
          session_id: session.session_id,
          sender: 'user',
          content,
          timestamp: new Date().toISOString(),
        };
        
        set((state) => ({
          messages: [...state.messages, userMessage],
          isLoading: true,
        }));
        
        try {
          // API 호출
          const response = await chatApi.sendMessage({
            session_id: session.session_id,
            content,
          });
          
          // AI/상담원 응답 추가
          const responseMessage: Message = {
            id: uuidv4(),
            session_id: session.session_id,
            sender: response.sender as 'ai' | 'agent',
            content: response.response,
            timestamp: new Date().toISOString(),
            is_answer: true,
          };
          
          set((state) => ({
            messages: [...state.messages, responseMessage],
            isLoading: false,
          }));
          
        } catch (error: any) {
          set({ 
            error: error.message || '메시지 전송 중 오류가 발생했습니다.',
            isLoading: false,
          });
          
          // 오류 메시지 추가
          const errorMessage: Message = {
            id: uuidv4(),
            session_id: session.session_id,
            sender: 'system',
            content: '메시지 전송에 실패했습니다. 다시 시도해주세요.',
            timestamp: new Date().toISOString(),
          };
          
          set((state) => ({
            messages: [...state.messages, errorMessage],
          }));
        }
      },

      endSession: async () => {
        const { session } = get();
        
        if (!session) return;
        
        try {
          await chatApi.endSession(session.session_id);
          
          set((state) => ({
            session: state.session ? {
              ...state.session,
              status: 'ended',
              ended_at: new Date().toISOString(),
            } : null,
          }));
          
          // 종료 메시지 추가
          const endMessage: Message = {
            id: uuidv4(),
            session_id: session.session_id,
            sender: 'system',
            content: '상담이 종료되었습니다. 감사합니다!',
            timestamp: new Date().toISOString(),
          };
          
          set((state) => ({
            messages: [...state.messages, endMessage],
          }));
          
        } catch (error: any) {
          set({ error: error.message || '세션 종료 중 오류가 발생했습니다.' });
        }
      },

      reset: () => {
        set({
          user: null,
          session: null,
          messages: [],
          isLoading: false,
          error: null,
        });
      },
    }),
    {
      name: 'chat-store',
    }
  )
);