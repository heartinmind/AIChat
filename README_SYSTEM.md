# Elite Beauty Clinic AI 상담 시스템

## 📋 시스템 구성

- **Backend API**: FastAPI + SQLAlchemy + Claude AI
- **Admin Dashboard**: React + TypeScript + Material-UI
- **Database**: SQLite (개발용) / PostgreSQL (프로덕션)

## 🚀 빠른 시작

### 1. 시스템 시작
```bash
cd /Users/unipurple/Projects/AIChat
./start_system_v2.sh
```

### 2. 시스템 상태 확인
```bash
./check_status.sh
```

### 3. 시스템 종료
```bash
./stop_system.sh
```

## 🌐 접속 정보

- **Backend API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **Admin Dashboard**: http://localhost:3000

## 👤 Admin 로그인 정보

- **이메일**: admin@elitebeauty.com
- **비밀번호**: admin123

## 📁 프로젝트 구조

```
AIChat/
├── backend/                # Backend API 서버
│   ├── main.py            # FastAPI 앱
│   ├── database/          # 데이터베이스 모델 및 연결
│   ├── create_admin.py    # Admin 계정 생성 스크립트
│   └── requirements.txt   # Python 패키지
├── admin/                 # Admin 대시보드
│   ├── src/              # React 소스 코드
│   │   ├── pages/        # 페이지 컴포넌트
│   │   ├── contexts/     # React Context
│   │   └── layouts/      # 레이아웃 컴포넌트
│   └── package.json      # npm 패키지
├── start_system_v2.sh    # 시스템 시작 스크립트
├── stop_system.sh        # 시스템 종료 스크립트
└── check_status.sh       # 상태 확인 스크립트
```

## 🛠️ 문제 해결

### Backend가 시작되지 않는 경우
1. Python 가상환경 확인:
```bash
source venv/bin/activate
pip install -r backend/requirements.txt
```

2. 직접 실행:
```bash
cd backend
python main.py
```

### Admin Dashboard가 시작되지 않는 경우
1. 패키지 재설치:
```bash
cd admin
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

2. 직접 실행:
```bash
npm start
```

### 포트가 이미 사용 중인 경우
```bash
# 8000 포트 프로세스 종료
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# 3000 포트 프로세스 종료
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

## 📝 환경 변수 설정

`.env` 파일을 생성하여 환경 변수를 설정할 수 있습니다:

```env
# AI API 키
CLAUDE_API_KEY=your-claude-api-key-here

# 보안 키
SECRET_KEY=your-secret-key-here

# 데이터베이스 URL (선택사항)
DATABASE_URL=sqlite:///./elite_beauty.db
```

## 🔧 개발 모드

### Backend 개발 서버
```bash
cd backend
uvicorn main:app --reload
```

### Frontend 개발 서버
```bash
cd admin
npm start
```

## 📚 주요 기능

### Admin Dashboard
- **Dashboard**: 실시간 상담 현황
- **Sessions**: 상담 내역 관리
- **Users**: 사용자 관리
- **Agents**: 상담원 관리
- **Analytics**: 통계 분석
- **RAG Management**: 문서 관리
- **Settings**: 시스템 설정

### Backend API
- 사용자 인증 및 세션 관리
- Claude AI 통합
- 실시간 상담 라우팅
- 통계 데이터 제공

## 📞 지원

문제가 있으시면 다음을 확인해주세요:
1. `./check_status.sh` 실행하여 시스템 상태 확인
2. 터미널 로그 확인
3. `.env` 파일 설정 확인
