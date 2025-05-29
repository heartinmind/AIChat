import React, { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/router';
import {
  Box,
  Container,
  Paper,
  Typography,
  TextField,
  IconButton,
  AppBar,
  Toolbar,
  Avatar,
  Chip,
  CircularProgress,
  Fade,
  Grow,
} from '@mui/material';
import {
  Send,
  ExitToApp,
  SmartToy,
  SupportAgent,
  Spa,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';
import { useChat } from '../contexts/ChatContext';

const ChatPage: React.FC = () => {
  const router = useRouter();
  const {
    user,
    session,
    messages,
    isLoading,
    createSession,
    sendMessage,
    endSession,
  } = useChat();

  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // 세션 생성
  useEffect(() => {
    if (!user) {
      router.push('/');
      return;
    }

    if (!session) {
      createSession();
    }
  }, [user, session, router, createSession]);

  // 자동 스크롤
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 메시지 전송 처리
  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputMessage.trim() || isLoading) return;

    const message = inputMessage;
    setInputMessage('');
    setIsTyping(true);

    try {
      await sendMessage(message);
    } catch (err) {
      // 에러는 context에서 처리됨
    } finally {
      setIsTyping(false);
      inputRef.current?.focus();
    }
  };

  // 세션 종료
  const handleEndSession = async () => {
    if (window.confirm('상담을 종료하시겠습니까?')) {
      await endSession();
      router.push('/');
    }
  };

  if (!user || !session) {
    return (
      <Box
        sx={{
          height: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* 헤더 */}
      <AppBar
        position="static"
        elevation={0}
        sx={{
          background: 'linear-gradient(135deg, #E91E63 0%, #9C27B0 100%)',
        }}
      >
        <Toolbar>
          <Spa sx={{ mr: 2 }} />
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            엘리트 뷰티 클리닉
          </Typography>

          <Chip
            icon={session.route_target === 'ai' ? <SmartToy /> : <SupportAgent />}
            label={session.route_target === 'ai' ? 'AI 상담사 지수' : '전문 상담사'}
            sx={{
              mr: 2,
              background: 'rgba(255, 255, 255, 0.2)',
              color: 'white',
            }}
          />

          <IconButton color="inherit" onClick={handleEndSession}>
            <ExitToApp />
          </IconButton>
        </Toolbar>
      </AppBar>

      {/* 메시지 영역 */}
      <Box
        sx={{
          flexGrow: 1,
          overflow: 'auto',
          p: 3,
          background: '#FAFAFA',
        }}
      >
        <Container maxWidth="md">
          {/* 환영 메시지 */}
          <Fade in timeout={1000}>
            <Box sx={{ textAlign: 'center', mb: 4 }}>
              <Typography variant="h5" color="text.secondary">
                안녕하세요, {user.name}님! 👋
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
                무엇을 도와드릴까요?
              </Typography>
            </Box>
          </Fade>

          {/* 메시지 목록 */}
          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={message.message_id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.05 }}
              >
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                    mb: 2,
                  }}
                >
                  {message.sender !== 'user' && (
                    <Avatar
                      sx={{
                        mr: 1,
                        bgcolor: message.sender === 'ai' ? 'secondary.main' : 'primary.main',
                      }}
                    >
                      {message.sender === 'ai' ? <SmartToy /> : <SupportAgent />}
                    </Avatar>
                  )}

                  <Paper
                    elevation={0}
                    sx={{
                      p: 2,
                      maxWidth: '70%',
                      borderRadius: 3,
                      bgcolor: message.sender === 'user' ? 'primary.main' : 'white',
                      color: message.sender === 'user' ? 'white' : 'text.primary',
                      borderBottomRightRadius: message.sender === 'user' ? 4 : 16,
                      borderBottomLeftRadius: message.sender === 'user' ? 16 : 4,
                    }}
                  >
                    <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                      {message.content}
                    </Typography>
                    <Typography
                      variant="caption"
                      sx={{
                        display: 'block',
                        mt: 1,
                        opacity: 0.7,
                      }}
                    >
                      {format(new Date(message.timestamp), 'a h:mm', { locale: ko })}
                    </Typography>
                  </Paper>

                  {message.sender === 'user' && (
                    <Avatar sx={{ ml: 1, bgcolor: 'grey.400' }}>
                      {user.name[0]}
                    </Avatar>
                  )}
                </Box>
              </motion.div>
            ))}
          </AnimatePresence>

          {/* 타이핑 인디케이터 */}
          {isTyping && (
            <Grow in>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ mr: 1, bgcolor: 'secondary.main' }}>
                  <SmartToy />
                </Avatar>
                <Paper
                  elevation={0}
                  sx={{
                    p: 2,
                    borderRadius: 3,
                    bgcolor: 'white',
                  }}
                >
                  <Box sx={{ display: 'flex', gap: 0.5 }}>
                    <motion.div
                      animate={{ y: [0, -5, 0] }}
                      transition={{ duration: 0.6, repeat: Infinity, delay: 0 }}
                    >
                      <Box
                        sx={{
                          width: 8,
                          height: 8,
                          borderRadius: '50%',
                          bgcolor: 'text.secondary',
                        }}
                      />
                    </motion.div>
                    <motion.div
                      animate={{ y: [0, -5, 0] }}
                      transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }}
                    >
                      <Box
                        sx={{
                          width: 8,
                          height: 8,
                          borderRadius: '50%',
                          bgcolor: 'text.secondary',
                        }}
                      />
                    </motion.div>
                    <motion.div
                      animate={{ y: [0, -5, 0] }}
                      transition={{ duration: 0.6, repeat: Infinity, delay: 0.4 }}
                    >
                      <Box
                        sx={{
                          width: 8,
                          height: 8,
                          borderRadius: '50%',
                          bgcolor: 'text.secondary',
                        }}
                      />
                    </motion.div>
                  </Box>
                </Paper>
              </Box>
            </Grow>
          )}

          <div ref={messagesEndRef} />
        </Container>
      </Box>

      {/* 입력 영역 */}
      <Paper
        elevation={3}
        sx={{
          p: 2,
          borderRadius: 0,
        }}
      >
        <Container maxWidth="md">
          <form onSubmit={handleSendMessage}>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <TextField
                ref={inputRef}
                fullWidth
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="메시지를 입력하세요..."
                disabled={isLoading}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    borderRadius: 3,
                    bgcolor: 'grey.100',
                    '& fieldset': {
                      border: 'none',
                    },
                  },
                }}
              />
              <IconButton
                type="submit"
                disabled={!inputMessage.trim() || isLoading}
                sx={{
                  bgcolor: 'primary.main',
                  color: 'white',
                  '&:hover': {
                    bgcolor: 'primary.dark',
                  },
                  '&:disabled': {
                    bgcolor: 'grey.300',
                    color: 'grey.500',
                  },
                }}
              >
                <Send />
              </IconButton>
            </Box>
          </form>
        </Container>
      </Paper>
    </Box>
  );
};

export default ChatPage;
