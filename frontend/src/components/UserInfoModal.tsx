import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { useChatStore } from '@/stores/chatStore';
import toast from 'react-hot-toast';

interface UserInfoModalProps {
  isOpen: boolean;
  onClose: () => void;
  onComplete: () => void;
}

interface UserFormData {
  name: string;
  phone: string;
  gender?: string;
  birthYear?: number;
}

const UserInfoModal: React.FC<UserInfoModalProps> = ({ isOpen, onClose, onComplete }) => {
  const { register, handleSubmit, formState: { errors } } = useForm<UserFormData>();
  const { initializeChat } = useChatStore();

  const onSubmit = async (data: UserFormData) => {
    try {
      await initializeChat(data);
      toast.success('상담을 시작합니다!');
      onComplete();
    } catch (error) {
      toast.error('오류가 발생했습니다. 다시 시도해주세요.');
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 z-50"
            onClick={onClose}
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white rounded-2xl p-6 w-96 z-50"
          >
            <h2 className="text-2xl font-bold mb-4 text-gray-800">상담 시작하기</h2>
            <p className="text-gray-600 mb-6">
              더 나은 상담을 위해 간단한 정보를 입력해주세요.
            </p>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  이름 <span className="text-red-500">*</span>
                </label>
                <input
                  {...register('name', { required: '이름을 입력해주세요' })}
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="홍길동"
                />
                {errors.name && (
                  <p className="text-red-500 text-xs mt-1">{errors.name.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  연락처 <span className="text-red-500">*</span>
                </label>
                <input
                  {...register('phone', {
                    required: '연락처를 입력해주세요',
                    pattern: {
                      value: /^01[0-9]-?[0-9]{3,4}-?[0-9]{4}$/,
                      message: '올바른 휴대폰 번호를 입력해주세요',
                    },
                  })}
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="010-1234-5678"
                />
                {errors.phone && (
                  <p className="text-red-500 text-xs mt-1">{errors.phone.message}</p>
                )}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    성별 (선택)
                  </label>
                  <select
                    {...register('gender')}
                    className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  >
                    <option value="">선택안함</option>
                    <option value="여성">여성</option>
                    <option value="남성">남성</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    출생연도 (선택)
                  </label>
                  <input
                    {...register('birthYear', {
                      min: { value: 1900, message: '올바른 연도를 입력해주세요' },
                      max: { value: new Date().getFullYear(), message: '올바른 연도를 입력해주세요' },
                    })}
                    type="number"
                    className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="1990"
                  />
                  {errors.birthYear && (
                    <p className="text-red-500 text-xs mt-1">{errors.birthYear.message}</p>
                  )}
                </div>
              </div>

              <div className="flex gap-3 mt-6">
                <button
                  type="button"
                  onClick={onClose}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  취소
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-gradient-to-r from-pink-500 to-purple-600 text-white rounded-lg hover:shadow-lg transition-all"
                >
                  상담 시작
                </button>
              </div>
            </form>

            <p className="text-xs text-gray-500 mt-4 text-center">
              * 입력하신 정보는 상담 목적으로만 사용됩니다
            </p>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default UserInfoModal;