# Elite Beauty Clinic AI Chat System - 핸드오버 문서

## 🔗 프로젝트 정보
- **프로젝트 경로**: `/Users/unipurple/Projects/AIChat`
- **GitHub 저장소**: (Push 후 URL 입력)

## 🏗️ 시스템 아키텍처

### Backend (FastAPI)
- **포트**: 8000
- **주요 파일**: `backend/main.py`
- **데이터베이스**: SQLite (`elite_beauty.db`)
- **인증**: JWT Bearer Token
- **AI**: Claude API (claude-3-5-sonnet-20241022)

### Frontend - 사용자 채팅 (Next.js)
- **포트**: 3002
- **주요 파일**: `frontend/src/components/ChatInterface.tsx`
- **상태 관리**: React Hooks + Context
- **API 통신**: Axios

### Frontend - 관리자 대시보드 (React)
- **포트**: 3001
- **주요 파일**: `admin/src/App.tsx`
- **UI 라이브러리**: Material-UI
- **라우팅**: React Router v6

## 🔑 주요 API 엔드포인트

### 인증
- `POST /api/agents/login` - 관리자 로그인

### 채팅
- `POST /api/session/route` - 라우팅 결정 (AI/상담원)
- `POST /api/users` - 사용자 생성/조회
- `POST /api/sessions` - 세션 생성
- `POST /api/messages` - 메시지 전송
- `GET /api/sessions/{session_id}/messages` - 메시지 조회

### 관리자
- `GET /api/admin/dashboard` - 대시보드 통계
- `GET /api/admin/sessions` - 세션 목록
- `GET /api/admin/users` - 사용자 목록
- `GET /api/admin/agents` - 상담원 목록

## 📦 필요한 패키지

### Python (Backend)
```
fastapi==0.115.5
uvicorn[standard]==0.32.1
sqlalchemy==2.0.36
anthropic==0.39.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
```

### Node.js (Frontend)
```
# 사용자 채팅
next@14.0.3
react@18.2.0
socket.io-client@4.5.4

# 관리자 대시보드
@mui/material@5.14.20
recharts@2.10.3
react-router-dom@6.20.0
```

## 🚀 WebSocket 구현 계획

### 1. Backend 수정 필요사항
- FastAPI WebSocket 엔드포인트 추가
- 연결 관리자 (ConnectionManager) 구현
- 실시간 메시지 브로드캐스팅

### 2. Frontend 수정 필요사항
- Socket.io-client 통합
- 실시간 메시지 수신 처리
- 연결 상태 표시
- 재연결 로직

### 3. 데이터베이스 스키마 추가
- `agent_sessions` 테이블 (상담원 세션 관리)
- `session_status` 업데이트 로직

## 🎨 UI 개선 우선순위

### 사용자 채팅 (frontend)
1. 모바일 반응형 개선
2. 다크 모드 지원
3. 이모티콘/파일 업로드
4. 타이핑 인디케이터
5. 음성 메시지

### 관리자 대시보드 (admin)
1. 실시간 대시보드 업데이트
2. 상담원별 성과 지표
3. 상담 내역 검색/필터 강화
4. 리포트 다운로드 기능
5. 상담원 상태 관리 UI

## 🔧 환경 설정

### 개발 환경
- Python 3.13 (3.12도 가능)
- Node.js 18+
- npm 또는 yarn

### 필수 환경 변수
```bash
# Backend
CLAUDE_API_KEY=실제_API_키
SECRET_KEY=JWT_시크릿_키
DATABASE_URL=sqlite:///./elite_beauty.db

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📝 테스트 계정
- **관리자**: admin@elitebeauty.com / admin123

## 🐛 알려진 이슈

1. **상담원 상태 변경 버튼 미구현**
   - 위치: Admin Dashboard > Agents
   - API는 준비됨, UI만 추가 필요

2. **실시간 업데이트 없음**
   - 현재 폴링 방식
   - WebSocket 구현 필요

3. **파일 업로드 미구현**
   - Backend API 추가 필요
   - Frontend UI 추가 필요

## 💡 개발 팁

1. **Backend 변경 시**
   - Uvicorn이 자동 리로드됨
   - 로그: `tail -f backend.log`

2. **Frontend 변경 시**
   - Next.js/React 핫 리로드 작동
   - 브라우저 자동 새로고침

3. **데이터베이스 초기화**
   ```bash
   cd backend
   rm elite_beauty.db
   PYTHONPATH=. python create_admin.py
   ```

## 🚨 주의사항

1. **API 키 보안**
   - 절대 커밋하지 말 것
   - .env 파일 확인 필수

2. **CORS 설정**
   - 프로덕션 배포 시 수정 필요
   - 현재 모든 origin 허용 상태

3. **데이터베이스**
   - SQLite는 개발용
   - 프로덕션은 PostgreSQL 권장

## 📞 연락처
- 프로젝트 관련 문의: [작성자 이메일]
- 기술 지원: [팀 Slack/Discord]
