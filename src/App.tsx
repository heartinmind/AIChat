import React from 'react';
import ChatWidget from './components/ChatWidget';
import './App.css';

// AIChat 백엔드 API 호출 함수
const sendMessageToAI = async (message: string): Promise<string> => {
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    return data.response;
  } catch (error) {
    console.error('Error:', error);
    return '죄송합니다. 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.';
  }
};

function App() {
  return (
    <div className="App">
      {/* 메인 콘텐츠 */}
      <header className="App-header">
        <h1>엘리트 뷰티 클리닉</h1>
        <p>아름다움을 위한 당신의 선택</p>
      </header>

      <main>
        {/* 페이지 콘텐츠 */}
        <section className="hero">
          <h2>프리미엄 뷰티 케어</h2>
          <p>최신 기술과 전문 의료진이 함께합니다</p>
        </section>

        <section className="services">
          <h3>주요 시술</h3>
          <div className="service-grid">
            <div className="service-card">
              <h4>보톡스</h4>
              <p>주름 개선 및 예방</p>
            </div>
            <div className="service-card">
              <h4>필러</h4>
              <p>볼륨 개선 및 윤곽 교정</p>
            </div>
            <div className="service-card">
              <h4>레이저</h4>
              <p>피부 톤 개선 및 재생</p>
            </div>
          </div>
        </section>
      </main>

      {/* 채팅 위젯 */}
      <ChatWidget
        title="AI 뷰티 상담"
        subtitle="24시간 실시간 상담 가능"
        welcomeMessage="안녕하세요! 엘리트 뷰티 클리닉 AI 상담사입니다. 어떤 시술에 관심이 있으신가요?"
        placeholder="궁금한 점을 물어보세요..."
        botName="뷰티 AI"
        botAvatar="💆‍♀️"
        userAvatar="👤"
        onSendMessage={sendMessageToAI}
      />
    </div>
  );
}

export default App;
