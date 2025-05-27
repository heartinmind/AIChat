# AIChat 채팅 위젯 UI 가이드 💬

## 개요
Crisp 스타일의 모던한 채팅 위젯 UI를 AIChat 프로젝트에 적용했습니다.

## 주요 특징 ✨

### 1. **디자인**
- **다크 모드 기본** - 세련된 다크 테마
- **라이트 모드 지원** - 시스템 설정에 따라 자동 전환
- **부드러운 애니메이션** - 채팅창 열림/닫힘 효과
- **반응형 디자인** - 모바일 최적화

### 2. **기능**
- **플로팅 버튼** - 우측 하단 고정
- **실시간 타이핑 인디케이터** - AI가 답변 중임을 표시
- **자동 스크롤** - 새 메시지 자동 포커스
- **엔터키 전송** - 빠른 메시지 입력

### 3. **커스터마이징**
```tsx
<ChatWidget
  title="AI 뷰티 상담"
  subtitle="24시간 실시간 상담 가능"
  welcomeMessage="안녕하세요! 무엇을 도와드릴까요?"
  placeholder="메시지를 입력하세요..."
  botName="AI 상담사"
  botAvatar="🤖"
  userAvatar="👤"
  onSendMessage={handleMessage}
/>
```

## 설치 및 사용법 🚀

### 1. **필요한 파일들**
- `/src/components/ChatWidget.tsx` - 메인 컴포넌트
- `/src/styles/chat-widget.css` - 스타일시트
- `/src/App.tsx` - 사용 예시

### 2. **백엔드 연동**
```typescript
// API 호출 함수 예시
const sendMessageToAI = async (message: string): Promise<string> => {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });
  
  const data = await response.json();
  return data.response;
};
```

### 3. **스타일 커스터마이징**
CSS 변수를 통해 쉽게 색상 변경 가능:
```css
:root {
  --chat-primary: #2c2c2e;      /* 메인 배경색 */
  --chat-accent: #007aff;       /* 강조 색상 */
  --chat-text-primary: #ffffff; /* 텍스트 색상 */
}
```

## 개선 사항 및 추가 기능 🔧

### 현재 구현된 기능
- ✅ 기본 채팅 UI
- ✅ 메시지 송수신
- ✅ 타이핑 인디케이터
- ✅ 반응형 디자인
- ✅ 다크/라이트 모드

### 추가 가능한 기능
- 📎 파일 첨부
- 🖼️ 이미지 미리보기
- 🔔 알림음
- 💾 대화 내역 저장
- 🌐 다국어 지원
- 📱 모바일 앱 딥링크
- 🎤 음성 입력
- 📤 대화 내보내기

## 백엔드 통합 예시 🔌

### Python Flask 서버 예시
```python
from flask import Flask, request, jsonify
from customer_service.agent import get_ai_response

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    message = request.json.get('message')
    
    # AI 응답 생성
    response = get_ai_response(message)
    
    return jsonify({
        'response': response,
        'timestamp': datetime.now().isoformat()
    })
```

### 실시간 통신 (WebSocket)
```typescript
// Socket.io 연동 예시
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

socket.on('message', (data) => {
  // 실시간 메시지 처리
});
```

## 성능 최적화 팁 ⚡

1. **메시지 가상화** - 많은 메시지 처리 시 react-window 사용
2. **이미지 레이지 로딩** - 이미지 첨부 시 지연 로딩
3. **메모이제이션** - React.memo로 불필요한 리렌더링 방지
4. **디바운싱** - 타이핑 중 API 호출 최적화

## 접근성 고려사항 ♿

- **키보드 네비게이션** 지원
- **스크린 리더** 호환
- **고대비 모드** 지원
- **포커스 관리** 적절한 포커스 이동

## 보안 고려사항 🔒

- **XSS 방지** - 사용자 입력 sanitize
- **CSRF 토큰** - API 요청 시 토큰 검증
- **Rate Limiting** - 스팸 방지
- **HTTPS 필수** - 모든 통신 암호화

## 테스트 🧪

```bash
# 컴포넌트 테스트
npm test ChatWidget.test.tsx

# E2E 테스트
npm run cypress
```

## 배포 준비 사항 📦

1. **환경 변수 설정**
   ```env
   REACT_APP_API_URL=https://api.elitebeauty.com
   REACT_APP_WEBSOCKET_URL=wss://ws.elitebeauty.com
   ```

2. **빌드 최적화**
   ```bash
   npm run build
   ```

3. **CDN 설정** - 정적 자원 CDN 배포

## 문제 해결 🛠️

### 채팅창이 안 열릴 때
- z-index 충돌 확인
- CSS 파일 import 확인

### 메시지가 전송되지 않을 때
- API 엔드포인트 확인
- CORS 설정 확인

### 스타일이 깨질 때
- CSS 변수 지원 브라우저 확인
- 전역 스타일 충돌 확인

---

이 UI는 실제 프로덕션에서 사용할 수 있는 수준으로 설계되었습니다.
추가 커스터마이징이 필요하시면 언제든 문의해주세요! 🎨
