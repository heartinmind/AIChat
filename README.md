# Elite Beauty Clinic AI Chat System

AI 기반 뷰티 클리닉 상담 시스템

## 🚀 주요 기능

- **AI 상담**: Claude AI를 활용한 24/7 자동 상담
- **실시간 상담원 연결**: 근무 시간 내 상담원 실시간 채팅
- **관리자 대시보드**: 상담 내역 관리 및 통계 분석
- **반응형 디자인**: 모바일/데스크톱 최적화

## 🛠️ 기술 스택

### Backend
- FastAPI (Python 3.9-3.12 권장, 3.13은 호환성 이슈 있음)
- SQLAlchemy + SQLite
- Claude AI API
- JWT Authentication

### Frontend
- **사용자 채팅**: Next.js 14 + TypeScript
- **관리자 대시보드**: React 18 + Material-UI
- **스타일링**: Tailwind CSS, Emotion

## 📦 설치 방법

### 사전 요구사항
- Python 3.9-3.12 (현재 Python 3.13은 일부 패키지와 호환성 문제가 있습니다)
- Node.js 18.x 이상
- Git

### Python 3.12 설치 (권장)
```bash
# macOS (Homebrew)
brew install python@3.12

# 또는 pyenv 사용
pyenv install 3.12.1
pyenv local 3.12.1
```

### 1. 저장소 클론
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 2. 초기 설정
```bash
chmod +x setup.sh
./setup.sh
```

### 3. 환경 변수 설정
`.env` 파일을 열어 필요한 API 키를 입력:
```
CLAUDE_API_KEY=your-actual-api-key-here
```

### 4. 시스템 시작
```bash
./start_all.sh
```

## 🌐 접속 URL

- **사용자 채팅**: http://localhost:3002
- **관리자 대시보드**: http://localhost:3001
- **API 문서**: http://localhost:8000/docs

### 관리자 로그인
- 이메일: admin@elitebeauty.com
- 비밀번호: admin123

## 📁 프로젝트 구조

```
.
├── backend/            # FastAPI 백엔드
│   ├── main.py        # 메인 애플리케이션
│   ├── database/      # 데이터베이스 모델
│   └── requirements_py313.txt
│
├── frontend/          # Next.js 사용자 채팅
│   ├── src/
│   └── package.json
│
├── admin/            # React 관리자 대시보드
│   ├── src/
│   └── package.json
│
└── scripts/          # 유틸리티 스크립트
    ├── setup.sh
    ├── start_all.sh
    └── stop_all.sh
```

## 🔧 개발 명령어

```bash
# 전체 시스템 시작
./start_all.sh

# 전체 시스템 종료
./stop_all.sh

# 개별 테스트
bash test_backend_local.sh   # Backend 로컬 테스트

# 로그 확인
tail -f backend.log    # Backend 로그
tail -f admin.log      # Admin 로그
tail -f frontend.log   # Frontend 로그
```

### 트러블슈팅

#### Python 3.13 호환성 문제
```bash
# Python 버전 확인
python3 --version

# Python 3.12 설치 가이드 실행
bash install_python312.sh
```

#### 포트 충돌
```bash
# 8000번 포트 사용 프로세스 확인
lsof -i :8000

# 프로세스 종료
kill -9 $(lsof -ti :8000)
```

## 📋 개발 로드맵

- [x] 기본 채팅 시스템
- [x] AI 통합
- [x] 관리자 대시보드
- [ ] WebSocket 실시간 통신
- [ ] 상담원 대시보드
- [ ] 근무시간 관리
- [ ] 고급 분석 기능

자세한 내용은 [ROADMAP.md](./ROADMAP.md) 참조

## 🤝 기여 방법

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다.

## 👥 팀

- 개발팀: Elite Beauty Tech Team
- 문의: admin@elitebeauty.com
