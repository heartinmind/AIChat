import React from 'react';
import { motion } from 'framer-motion';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';
import { Message } from '@/types';

interface MessageListProps {
  messages: Message[];
}

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  return (
    <div className="space-y-4">
      {messages.map((message, index) => (
        <motion.div
          key={message.id}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.05 }}
          className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <div
            className={`max-w-[80%] rounded-2xl px-4 py-2 ${
              message.sender === 'user'
                ? 'bg-gradient-to-r from-pink-500 to-purple-600 text-white'
                : message.sender === 'ai'
                ? 'bg-white shadow-md'
                : 'bg-gray-200'
            }`}
          >
            <p className="text-sm whitespace-pre-wrap">{message.content}</p>
            <p
              className={`text-xs mt-1 ${
                message.sender === 'user' ? 'text-white/70' : 'text-gray-500'
              }`}
            >
              {format(new Date(message.timestamp), 'HH:mm', { locale: ko })}
            </p>
          </div>
        </motion.div>
      ))}
      
      {messages.length === 0 && (
        <div className="text-center text-gray-500 py-8">
          <p className="text-lg mb-2">안녕하세요! 👋</p>
          <p className="text-sm">엘리트 뷰티 클리닉 AI 상담사입니다.</p>
          <p className="text-sm">무엇을 도와드릴까요?</p>
        </div>
      )}
    </div>
  );
};

export default MessageList;