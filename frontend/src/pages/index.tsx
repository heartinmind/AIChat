import React from 'react';
import Head from 'next/head';
import LandingPage from '@/components/LandingPage';

export default function Home() {
  return (
    <>
      <Head>
        <title>엘리트 뷰티 클리닉 - AI 상담</title>
        <meta name="description" content="24시간 AI 뷰티 상담 서비스" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <main>
        <LandingPage />
      </main>
    </>
  );
}
