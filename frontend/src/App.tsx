import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';
import ChatPage from './pages/ChatPage';
import LandingPage from './pages/LandingPage';
import { ChatProvider } from './contexts/ChatContext';

function App() {
  return (
    <ChatProvider>
      <Box
        sx={{
          minHeight: '100vh',
          background: 'linear-gradient(135deg, #FAFAFA 0%, #FFF0F5 100%)',
        }}
      >
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/chat" element={<ChatPage />} />
        </Routes>
      </Box>
    </ChatProvider>
  );
}

export default App;
