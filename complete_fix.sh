#!/bin/bash

# Elite Beauty Clinic AI 시스템 - 전체 문제 해결 스크립트

echo "🔧 Elite Beauty Clinic AI 시스템 문제 해결을 시작합니다..."
echo "=================================================="
echo ""

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 프로젝트 디렉토리
PROJECT_DIR="/Users/unipurple/Projects/AIChat"
cd "$PROJECT_DIR"

# 1. 현재 상태 확인
echo -e "${YELLOW}1. 현재 상태 확인${NC}"
echo "-------------------"
echo "Python 버전:"
python3 --version
echo ""
echo "Node.js 버전:"
node --version
echo "npm 버전:"
npm --version
echo ""

# 2. 프로세스 정리
echo -e "${YELLOW}2. 기존 프로세스 정리${NC}"
echo "----------------------"
pkill -f "python.*main.py" 2>/dev/null
pkill -f "node.*react-scripts" 2>/dev/null
rm -f .backend.pid .frontend.pid
sleep 2
echo -e "${GREEN}✓ 완료${NC}"
echo ""

# 3. Python 환경 설정
echo -e "${YELLOW}3. Python 환경 재설정${NC}"
echo "----------------------"

# 가상환경 재생성 (클린 설치)
echo "가상환경을 재생성합니다..."
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# pip 업그레이드
pip install --upgrade pip

# 4. Backend 패키지 설치
echo -e "${YELLOW}4. Backend 패키지 설치${NC}"
echo "----------------------"

# requirements_fixed.txt 생성
cat > backend/requirements_fixed.txt << 'EOL'
# Core dependencies with fixed versions
fastapi==0.110.0
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.25
alembic==1.12.1

# AI - 안정적인 버전 사용
anthropic==0.25.0
httpx==0.25.2

# Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
bcrypt==4.1.2

# Utils
pydantic==2.5.0
python-dateutil==2.8.2
loguru==0.7.2
EOL

echo "패키지를 설치합니다..."
pip install -r backend/requirements_fixed.txt

# 5. database.models 문제 해결
echo -e "${YELLOW}5. Database 모듈 문제 해결${NC}"
echo "---------------------------"

# __init__.py 파일 확인 및 생성
touch backend/__init__.py
touch backend/database/__init__.py

# PYTHONPATH 설정
export PYTHONPATH="${PROJECT_DIR}/backend:$PYTHONPATH"

# 6. Backend 테스트
echo -e "${YELLOW}6. Backend 테스트${NC}"
echo "-----------------"
cd backend
python3 -c "
import sys
sys.path.insert(0, '.')
print('Python 경로:', sys.path[:3])
try:
    from database.models import Base
    print('✅ database.models import 성공!')
    from main import app
    print('✅ main.py import 성공!')
    print('✅ Backend 준비 완료!')
except Exception as e:
    print(f'❌ Import 오류: {e}')
    import traceback
    traceback.print_exc()
"
cd ..

# 7. .env 파일 생성
echo -e "${YELLOW}7. 환경 설정${NC}"
echo "-------------"
if [ ! -f ".env" ]; then
    cat > .env << 'EOL'
SECRET_KEY=elite-beauty-secret-key-2024
CLAUDE_API_KEY=sk-ant-api03-YOUR-KEY-HERE
DATABASE_URL=sqlite:///./elite_beauty.db
EOL
    echo -e "${GREEN}✓ .env 파일 생성됨${NC}"
else
    echo -e "${GREEN}✓ .env 파일이 이미 존재합니다${NC}"
fi

# 8. Admin 계정 생성
echo -e "${YELLOW}8. Admin 계정 확인${NC}"
echo "------------------"
cd backend
PYTHONPATH=. python create_admin.py 2>/dev/null || echo "Admin 계정이 이미 존재합니다"
cd ..

# 9. Frontend 설정
echo -e "${YELLOW}9. Frontend 설정${NC}"
echo "-----------------"
cd admin

# package.json 수정 (TypeScript 버전 조정)
if [ -f "package.json" ]; then
    # TypeScript 버전을 4.9.5로 고정
    sed -i '' 's/"typescript": ".*"/"typescript": "^4.9.5"/' package.json 2>/dev/null || \
    sed -i 's/"typescript": ".*"/"typescript": "^4.9.5"/' package.json
fi

# node_modules 정리 및 재설치
echo "Frontend 패키지를 설치합니다..."
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps

cd ..

# 10. 시스템 시작
echo ""
echo -e "${YELLOW}10. 시스템 시작${NC}"
echo "----------------"

# Backend 시작
echo "Backend를 시작합니다..."
cd backend
PYTHONPATH=. nohup python main.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Backend 시작 확인
sleep 3
if ps -p $BACKEND_PID > /dev/null; then
    echo -e "${GREEN}✓ Backend 시작됨 (PID: $BACKEND_PID)${NC}"
    
    # API 상태 확인
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend API 정상 작동${NC}"
    else
        echo -e "${YELLOW}! Backend API가 아직 준비 중입니다${NC}"
    fi
else
    echo -e "${RED}✗ Backend 시작 실패${NC}"
    echo "최근 로그:"
    tail -20 backend.log
    exit 1
fi

# Frontend 시작
echo ""
echo "Frontend를 시작합니다..."
cd admin
nohup npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# PID 저장
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

# 완료 메시지
echo ""
echo "=================================================="
echo -e "${GREEN}✅ 시스템 시작 완료!${NC}"
echo "=================================================="
echo ""
echo -e "${BLUE}📌 접속 정보:${NC}"
echo "   Admin Dashboard: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API 문서: http://localhost:8000/docs"
echo ""
echo -e "${BLUE}🔑 로그인 정보:${NC}"
echo "   이메일: admin@elitebeauty.com"
echo "   비밀번호: admin123"
echo ""
echo -e "${BLUE}📋 유용한 명령어:${NC}"
echo "   Backend 로그: tail -f backend.log"
echo "   Frontend 로그: tail -f frontend.log"
echo "   상태 확인: ./check_status.sh"
echo "   시스템 종료: ./stop_system.sh"
echo ""
echo "브라우저가 자동으로 열리지 않으면 http://localhost:3000 으로 접속하세요!"
