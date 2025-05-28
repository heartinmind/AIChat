import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  TextField,
  Button,
  Paper,
  Grid,
  InputAdornment,
  Alert,
  CircularProgress,
} from '@mui/material';
import { Person, Phone, Spa, AutoAwesome } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useChat } from '../contexts/ChatContext';

const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const { createUser, isLoading, error } = useChat();
  
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [localError, setLocalError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError('');

    // 유효성 검사
    if (!name.trim()) {
      setLocalError('이름을 입력해주세요.');
      return;
    }

    if (!phone.trim() || !/^010-?\d{4}-?\d{4}$/.test(phone.replace(/-/g, ''))) {
      setLocalError('올바른 휴대폰 번호를 입력해주세요.');
      return;
    }

    try {
      await createUser(name, phone);
      navigate('/chat');
    } catch (err) {
      // 에러는 context에서 처리됨
    }
  };

  return (
    <Container maxWidth="lg" sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center' }}>
      <Grid container spacing={6} alignItems="center">
        {/* 왼쪽: 브랜딩 섹션 */}
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >
            <Box sx={{ mb: 4 }}>
              <Typography
                variant="h1"
                sx={{
                  background: 'linear-gradient(135deg, #E91E63 0%, #9C27B0 100%)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  mb: 2,
                }}
              >
                엘리트 뷰티 클리닉
              </Typography>
              <Typography variant="h5" color="text.secondary" sx={{ mb: 3 }}>
                AI와 전문 상담사가 함께하는 맞춤형 뷰티 상담
              </Typography>
            </Box>

            <Grid container spacing={3}>
              <Grid item xs={12} sm={6}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Spa sx={{ fontSize: 40, color: 'primary.main' }} />
                  <Box>
                    <Typography variant="h6">맞춤형 시술</Typography>
                    <Typography variant="body2" color="text.secondary">
                      고객님께 최적화된 시술 추천
                    </Typography>
                  </Box>
                </Box>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <AutoAwesome sx={{ fontSize: 40, color: 'secondary.main' }} />
                  <Box>
                    <Typography variant="h6">24시간 AI 상담</Typography>
                    <Typography variant="body2" color="text.secondary">
                      언제든 편하게 문의하세요
                    </Typography>
                  </Box>
                </Box>
              </Grid>
            </Grid>
          </motion.div>
        </Grid>

        {/* 오른쪽: 로그인 폼 */}
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <Paper
              elevation={0}
              sx={{
                p: 6,
                borderRadius: 4,
                background: 'rgba(255, 255, 255, 0.9)',
                backdropFilter: 'blur(20px)',
                border: '1px solid rgba(233, 30, 99, 0.1)',
              }}
            >
              <Typography variant="h4" sx={{ mb: 1, fontWeight: 600 }}>
                상담 시작하기
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                간단한 정보 입력 후 바로 상담을 시작하세요
              </Typography>

              {(error || localError) && (
                <Alert severity="error" sx={{ mb: 3 }}>
                  {error || localError}
                </Alert>
              )}

              <form onSubmit={handleSubmit}>
                <TextField
                  fullWidth
                  label="이름"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  sx={{ mb: 3 }}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Person color="action" />
                      </InputAdornment>
                    ),
                  }}
                  disabled={isLoading}
                />

                <TextField
                  fullWidth
                  label="휴대폰 번호"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="010-1234-5678"
                  sx={{ mb: 4 }}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Phone color="action" />
                      </InputAdornment>
                    ),
                  }}
                  disabled={isLoading}
                />

                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  size="large"
                  disabled={isLoading}
                  sx={{
                    py: 2,
                    background: 'linear-gradient(135deg, #E91E63 0%, #9C27B0 100%)',
                    '&:hover': {
                      background: 'linear-gradient(135deg, #D81B60 0%, #8E24AA 100%)',
                    },
                  }}
                >
                  {isLoading ? (
                    <CircularProgress size={24} color="inherit" />
                  ) : (
                    '상담 시작하기'
                  )}
                </Button>
              </form>

              <Typography
                variant="caption"
                color="text.secondary"
                sx={{ display: 'block', mt: 3, textAlign: 'center' }}
              >
                상담 시작 시 개인정보 처리방침에 동의하는 것으로 간주됩니다
              </Typography>
            </Paper>
          </motion.div>
        </Grid>
      </Grid>
    </Container>
  );
};

export default LandingPage;
