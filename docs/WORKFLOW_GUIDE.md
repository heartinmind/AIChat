# AIChat 프로젝트 작업 가이드 🚀

## 협업 원칙

### 1. **역할 분담**
- **Claude (나)**: 
  - 전체 아키텍처 설계
  - 코드 리뷰 및 검증
  - 문제 해결 및 디버깅
  - 작업 지시 및 가이드
  
- **Cursor IDE**: 
  - 코드 자동완성 전용
  - 파일 열기/닫기
  - 단순 타이핑 작업

- **당신**: 
  - Claude와 대화
  - 최종 결정권자
  - 테스트 및 확인

### 2. **커뮤니케이션 규칙**
```
당신 ↔️ Claude (모든 대화)
  ↓
Claude → Cursor 지시 (필요시)
  ↓  
Cursor → 코드 작성
  ↓
Claude → 검증
  ↓
GitHub Push
```

## 작업 프로세스 📋

### 1. **작업 시작 전**
```bash
# 1. 최신 코드 받기
git pull origin main

# 2. 작업 브랜치 생성
git checkout -b feature/작업명

# 3. 환경 확인
python --version
node --version
```

### 2. **작업 중**
```bash
# 백업 생성 (중요 파일 수정 전)
cp 파일명 파일명.backup

# 작업 상태 자주 확인
git status

# 임시 저장
git stash
```

### 3. **작업 완료 후**
```bash
# 1. 테스트 실행
./run_tests.sh

# 2. 변경사항 확인
git diff

# 3. 커밋
git add .
git commit -m "[기능] 채팅 위젯 구현"

# 4. 푸시
git push origin feature/작업명

# 5. PR 생성 (GitHub에서)
```

## 파일 보호 체크리스트 ✅

### 절대 건드리면 안 되는 파일:
- [ ] `~/Library/Application Support/Claude/claude_desktop_config.json`
- [ ] `.env` (실제 환경변수)
- [ ] `service-account-key.json`
- [ ] `database/*.db`
- [ ] `*.pem`, `*.key` (인증서)

### 수정 전 백업 필수:
- [ ] `package.json`
- [ ] `requirements.txt`
- [ ] 설정 파일들
- [ ] 데이터베이스 스키마

## Cursor 설정 최적화 🔧

### 1. **settings.json에 추가**
```json
{
  "files.exclude": {
    "**/__pycache__": true,
    "**/node_modules": true,
    "**/.env": true
  },
  "editor.formatOnSave": true,
  "python.linting.enabled": true,
  "typescript.updateImportsOnFileMove.enabled": "always"
}
```

### 2. **확장 프로그램 권장**
- Python
- TypeScript
- GitLens
- Prettier
- ESLint

## 긴급 상황 대처법 🚨

### MCP 설정을 잘못 건드렸을 때:
```bash
# 1. Claude Desktop 종료
# 2. 백업에서 복원
cp ~/Desktop/claude_desktop_config.json.backup ~/Library/Application\ Support/Claude/claude_desktop_config.json
# 3. Claude Desktop 재시작
```

### 잘못된 커밋을 했을 때:
```bash
# 마지막 커밋 취소 (파일은 유지)
git reset --soft HEAD~1

# 마지막 커밋 완전 취소
git reset --hard HEAD~1
```

### 실수로 파일을 삭제했을 때:
```bash
# 특정 파일 복구
git checkout HEAD -- 파일명

# 모든 변경 취소
git checkout .
```

## 일일 체크리스트 📅

### 작업 시작 시:
- [ ] Git pull 실행
- [ ] 환경변수 확인
- [ ] 테스트 실행
- [ ] Claude와 오늘의 작업 논의

### 작업 종료 시:
- [ ] 모든 변경사항 커밋
- [ ] GitHub에 푸시
- [ ] 내일 작업 메모
- [ ] 중요 파일 백업

## 프로젝트 구조 이해하기 🏗️

```
AIChat/
├── src/                    # 메인 소스 코드
│   ├── components/        # React 컴포넌트
│   ├── styles/           # CSS 파일
│   └── utils/            # 유틸리티 함수
├── customer_service/      # 고객 서비스 모듈
│   ├── tools/            # 도구 함수
│   └── rag/              # RAG 시스템
├── database/             # DB 관련
├── templates/            # HTML 템플릿
├── tests/               # 테스트 파일
└── deployment/          # 배포 스크립트
```

## Git 커밋 메시지 템플릿 💬

```
[기능] 새로운 기능 추가
[수정] 버그 수정
[개선] 기능 개선
[리팩토링] 코드 정리
[문서] 문서 업데이트
[테스트] 테스트 추가/수정
[설정] 설정 파일 변경
[긴급] 핫픽스
```

## 명령어 모음 🛠️

```bash
# Python 가상환경
source venv/bin/activate  # 활성화
deactivate               # 비활성화

# 의존성 관리
pip install -r requirements.txt
pip freeze > requirements.txt

# Node.js
npm install
npm run build
npm start

# Docker
docker-compose up -d
docker-compose down
docker logs -f 컨테이너명

# 포트 확인
lsof -i :5000  # 5000번 포트 사용 프로세스
```

## 문제 발생 시 연락처 📞

1. **먼저 Claude에게 물어보기**
2. **GitHub Issues에 기록**
3. **팀 슬랙 채널에 공유** (있다면)

---

> 💡 **기억하세요**: 
> - 모든 대화는 Claude와!
> - Cursor는 타이핑 도구!
> - 커밋하고 푸시하기!
> - 백업은 생명입니다!

이 가이드를 항상 참고하면서 작업하세요. 
불확실한 것이 있으면 바로 물어보세요! 🚀
