# 🏥 Elite Beauty AI Chat System

> 엘리트 뷰티 클리닉 AI 하이브리드 상담 시스템 v1.0.0

## 📋 목차
- [개요](#개요)
- [주요 기능](#주요-기능)
- [시스템 아키텍처](#시스템-아키텍처)
- [설치 가이드](#설치-가이드)
- [실행 방법](#실행-방법)
- [프로젝트 구조](#프로젝트-구조)
- [API 문서](#api-문서)
- [트러블슈팅](#트러블슈팅)

## 개요

AI와 실제 상담원이 협업하는 하이브리드 채팅 시스템입니다. 근무 시간에는 상담원이, 그 외 시간에는 AI가 고객을 응대합니다.

### 시스템 특징
- 🤖 Claude AI 기반 자연스러운 대화
- 👥 실시간 상담원 연결
- 📱 반응형 웹 디자인
- 📊 관리자 대시보드
- 🔒 JWT 기반 보안 인증

## 주요 기능

### 1. 사용자 채팅
- 간편한 전화번호 인증
- AI/상담원 자동 라우팅
- 실시간 메시지 전송
- 대화 내역 저장

### 2. AI 상담
- 자연스러운 일상 대화
- 병원 정보 안내
- 시술 상담
- 24/7 운영

### 3. 관리자 기능
- 실시간 통계 대시보드
- 상담 내역 조회
- 사용자/상담원 관리
- 데이터 분석

## 시스템 아키텍처

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │     │   Backend   │     │  Database   │
│  (Next.js)  │────▶│  (FastAPI)  │────▶│  (SQLite)   │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Claude AI  │
                    └─────────────┘
```

## 설치 가이드

### 필수 요구사항
- Python 3.12 (3.13은 호환성 문제 있음)
- Node.js 18.x 이상
- Git

### 1. 프로젝트 클론
```bash
git clone <repository-url>
cd AIChat
```

### 2. Python 3.12 설치 (macOS)
```bash
brew install python@3.12
```

### 3. 가상환경 생성
```bash
python3.12 -m venv venv
source venv/bin/activate  # macOS/Linux
```

### 4. 백엔드 의존성 설치
```bash
cd backend
pip install -r requirements.txt
```

### 5. 프론트엔드 의존성 설치
```bash
cd ../frontend
npm install
```

### 6. 관리자 대시보드 의존성 설치
```bash
cd ../admin
npm install
```

### 7. 환경 변수 설정
```bash
# backend/.env 생성
CLAUDE_API_KEY=your-claude-api-key
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./elite_beauty.db

# frontend/.env.development 생성
NEXT_PUBLIC_API_URL=http://localhost:8000

# admin/.env 생성
REACT_APP_API_URL=http://localhost:8000
```

## 실행 방법

### 개별 실행

#### 1. 백엔드 서버
```bash
cd backend
source ../venv/bin/activate
uvicorn main:app --reload --port 8000
```

#### 2. 프론트엔드
```bash
cd frontend
npm run dev
```

#### 3. 관리자 대시보드
```bash
cd admin
npm start
```

### 전체 시스템 실행
```bash
# 프로젝트 루트에서
./start_all.sh
```

## 프로젝트 구조

```
AIChat/
├── backend/                 # FastAPI 백엔드
│   ├── main.py             # 메인 애플리케이션
│   ├── database/           # 데이터베이스 모델
│   │   ├── models.py       # SQLAlchemy 모델
│   │   └── connection.py   # DB 연결 설정
│   └── requirements.txt    # Python 의존성
│
├── frontend/               # Next.js 사용자 인터페이스
│   ├── src/
│   │   ├── app/           # 페이지 컴포넌트
│   │   ├── components/    # UI 컴포넌트
│   │   ├── contexts/      # React Context
│   │   ├── services/      # API 서비스
│   │   └── types/         # TypeScript 타입
│   └── package.json
│
├── admin/                  # React 관리자 대시보드
│   ├── src/
│   │   ├── components/    # 관리자 UI
│   │   ├── pages/        # 관리자 페이지
│   │   └── services/     # API 연동
│   └── package.json
│
├── docs/                   # 문서
├── scripts/               # 유틸리티 스크립트
└── README.md
```

## API 문서

### 주요 엔드포인트

#### 인증
- `POST /api/agents/login` - 상담원 로그인

#### 세션
- `POST /api/session/route` - 라우팅 확인
- `POST /api/sessions` - 세션 생성
- `GET /api/sessions/{id}/messages` - 메시지 조회

#### 메시지
- `POST /api/messages` - 메시지 전송

#### 사용자
- `POST /api/users` - 사용자 생성/조회

상세 API 문서: http://localhost:8000/docs

## 트러블슈팅

### Python 3.13 호환성 문제
```bash
# Python 3.12 설치
brew install python@3.12
python3.12 -m venv venv
```

### Anthropic 라이브러리 오류
```bash
pip install anthropic==0.18.1 httpx==0.24.1
```

### 포트 충돌
```bash
# 포트 확인
lsof -i :8000
# 프로세스 종료
kill -9 $(lsof -ti :8000)
```

## 📞 지원

- 이메일: admin@elitebeauty.com
- 개발팀: Elite Beauty Tech Team

## 📄 라이선스

Copyright © 2025 Elite Beauty Clinic. All rights reserved.
