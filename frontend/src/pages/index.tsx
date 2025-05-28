import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import ChatInterface from '@/components/ChatInterface';
import { Toaster } from 'react-hot-toast';

export default function Home() {
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  if (!isClient) {
    return null;
  }

  return (
    <>
      <Head>
        <title>엘리트 뷰티 클리닉 - AI 상담</title>
        <meta name="description" content="24시간 AI 뷰티 상담 서비스" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <main className="min-h-screen bg-gradient-to-br from-pink-50 to-purple-50">
        <Toaster position="top-right" />
        <ChatInterface />
      </main>
    </>
  );
}