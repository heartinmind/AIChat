import { useChatStore } from '@/stores/chatStore';

export const useChat = () => {
  const {
    user,
    session,
    messages,
    isLoading,
    error,
    initializeChat,
    sendMessage,
    endSession,
    reset,
  } = useChatStore();

  return {
    // State
    messages,
    isLoading,
    error,
    sessionInfo: session,
    userInfo: user,
    
    // Actions
    sendMessage,
    endSession,
    reset,
    initializeChat,
  };
};