import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useChat } from '@/hooks/useChat';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import UserInfoModal from './UserInfoModal';
import { ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline';

const ChatInterface: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [showUserInfo, setShowUserInfo] = useState(false);
  const { messages, sendMessage, isLoading, sessionInfo } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleOpen = () => {
    setIsOpen(true);
    if (!sessionInfo) {
      setShowUserInfo(true);
    }
  };

  const handleSendMessage = async (content: string) => {
    if (!sessionInfo && !showUserInfo) {
      setShowUserInfo(true);
      return;
    }
    await sendMessage(content);
  };

  return (
    <>
      {/* 플로팅 버튼 */}
      <AnimatePresence>
        {!isOpen && (
          <motion.button
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            exit={{ scale: 0 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={handleOpen}
            className="fixed bottom-6 right-6 w-16 h-16 bg-gradient-to-r from-pink-500 to-purple-600 rounded-full shadow-lg flex items-center justify-center text-white hover:shadow-xl transition-shadow"
          >
            <ChatBubbleLeftRightIcon className="w-8 h-8" />
          </motion.button>
        )}
      </AnimatePresence>

      {/* 채팅 창 */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.9 }}
            transition={{ type: 'spring', stiffness: 300, damping: 25 }}
            className="fixed bottom-6 right-6 w-96 h-[600px] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden"
          >
            {/* 헤더 */}
            <div className="bg-gradient-to-r from-pink-500 to-purple-600 p-4 text-white">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-bold">엘리트 뷰티 클리닉</h3>
                  <p className="text-sm opacity-90">AI 뷰티 상담사</p>
                </div>
                <button
                  onClick={() => setIsOpen(false)}
                  className="w-8 h-8 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center transition-colors"
                >
                  <span className="text-xl">×</span>
                </button>
              </div>
              {sessionInfo && (
                <div className="mt-2 flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  <span className="text-xs">{sessionInfo.route_target === 'ai' ? 'AI 상담중' : '상담원 연결중'}</span>
                </div>
              )}
            </div>

            {/* 메시지 영역 */}
            <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
              <MessageList messages={messages} />
              <div ref={messagesEndRef} />
            </div>

            {/* 입력 영역 */}
            <div className="p-4 bg-white border-t">
              <MessageInput 
                onSend={handleSendMessage} 
                disabled={isLoading || (!sessionInfo && !showUserInfo)}
                placeholder={sessionInfo ? "메시지를 입력하세요..." : "상담을 시작하려면 정보를 입력해주세요"}
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 사용자 정보 모달 */}
      <UserInfoModal
        isOpen={showUserInfo}
        onClose={() => setShowUserInfo(false)}
        onComplete={() => setShowUserInfo(false)}
      />
    </>
  );
};

export default ChatInterface;