# 🚨 Elite Beauty Clinic AI 시스템 - 문제 해결 가이드

## 현재 상황
1. **Backend 문제**: anthropic/httpx 버전 호환성 문제
2. **Frontend 문제**: TypeScript 버전 충돌
3. **경로 문제**: database.models 모듈 import 오류

## 🎯 해결 방법

### 옵션 1: 전체 시스템 재설정 (권장) ⭐
```bash
cd /Users/unipurple/Projects/AIChat
./complete_fix.sh
```
이 스크립트는 모든 문제를 자동으로 해결합니다.

### 옵션 2: 빠른 진단
```bash
cd /Users/unipurple/Projects/AIChat
./diagnose.sh
```
현재 시스템 상태를 확인합니다.

### 옵션 3: 수동 해결

#### Backend 수정:
```bash
cd /Users/unipurple/Projects/AIChat
source venv/bin/activate

# 패키지 재설치
pip uninstall -y anthropic httpx fastapi sqlalchemy
pip install fastapi==0.110.0 sqlalchemy==2.0.25 anthropic==0.25.0 httpx==0.25.2

# 실행
cd backend
PYTHONPATH=. python main.py
```

#### Frontend 수정:
```bash
cd /Users/unipurple/Projects/AIChat/admin
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
npm start
```

## 📋 체크리스트
- [ ] Python 3.x 설치됨
- [ ] Node.js 14+ 설치됨
- [ ] 가상환경 활성화됨
- [ ] .env 파일 존재
- [ ] 포트 8000, 3000 사용 가능

## 🔧 일반적인 오류 해결

### "ModuleNotFoundError: No module named 'database.models'"
```bash
cd backend
export PYTHONPATH=.
python main.py
```

### "TypeError: Client.__init__() got an unexpected keyword argument 'proxies'"
anthropic 버전 문제입니다. `./complete_fix.sh` 실행

### npm 의존성 오류
```bash
cd admin
npm install --legacy-peer-deps
```

## 🚀 빠른 시작
1. 터미널 열기
2. `cd /Users/unipurple/Projects/AIChat`
3. `./complete_fix.sh` 실행
4. 브라우저에서 http://localhost:3000 접속
5. 로그인: admin@elitebeauty.com / admin123

## 📞 추가 도움
- Backend 로그: `tail -f backend.log`
- Frontend 로그: `tail -f frontend.log`
- 시스템 종료: `./stop_system.sh`
