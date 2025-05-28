#!/bin/bash

# Elite Beauty Clinic AI 시스템 - 개선된 전체 문제 해결 스크립트

echo "🔧 Elite Beauty Clinic AI 시스템 문제 해결을 시작합니다 (v2)..."
echo "========================================================="
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

# 1. Python 설치 확인
echo -e "${YELLOW}1. Python 설치 확인${NC}"
echo "-------------------"

# Python 실행 파일 찾기
PYTHON_CMD=""
for py in python3.13 python3.12 python3.11 python3.10 python3.9 python3 python; do
    if command -v $py &> /dev/null; then
        echo -e "${GREEN}✓ $py 발견: $(which $py)${NC}"
        echo "  버전: $($py --version)"
        PYTHON_CMD=$py
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo -e "${RED}❌ Python이 설치되지 않았습니다!${NC}"
    echo "Homebrew로 설치: brew install python@3.12"
    exit 1
fi

echo ""
echo -e "${GREEN}사용할 Python: $PYTHON_CMD${NC}"
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

# 3. Python 가상환경 설정
echo -e "${YELLOW}3. Python 가상환경 재설정${NC}"
echo "--------------------------"

# 기존 가상환경 삭제
if [ -d "venv" ]; then
    echo "기존 가상환경을 삭제합니다..."
    rm -rf venv
fi

# 새 가상환경 생성
echo "새 가상환경을 생성합니다..."
$PYTHON_CMD -m venv venv

# 가상환경 생성 확인
if [ ! -f "venv/bin/activate" ]; then
    echo -e "${RED}❌ 가상환경 생성 실패!${NC}"
    echo "다음을 시도해보세요:"
    echo "1. $PYTHON_CMD -m pip install --user virtualenv"
    echo "2. $PYTHON_CMD -m virtualenv venv"
    exit 1
fi

echo -e "${GREEN}✓ 가상환경 생성 성공${NC}"

# 가상환경 활성화
echo "가상환경을 활성화합니다..."
source venv/bin/activate

# Python과 pip 경로 확인
echo "Python 경로: $(which python)"
echo "pip 경로: $(which pip)"

# pip 업그레이드
echo ""
echo "pip를 업그레이드합니다..."
python -m pip install --upgrade pip

# 4. Backend 패키지 설치
echo ""
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

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}일부 패키지 설치 실패. 개별 설치를 시도합니다...${NC}"
    pip install fastapi==0.110.0
    pip install uvicorn[standard]==0.24.0
    pip install sqlalchemy==2.0.25
    pip install anthropic==0.25.0
    pip install httpx==0.25.2
    pip install python-jose[cryptography]==3.3.0
    pip install passlib[bcrypt]==1.7.4
    pip install python-dotenv==1.0.0
    pip install pydantic==2.5.0
    pip install loguru==0.7.2
fi

# 5. database.models 문제 해결
echo ""
echo -e "${YELLOW}5. Database 모듈 문제 해결${NC}"
echo "---------------------------"

# __init__.py 파일 확인 및 생성
touch backend/__init__.py
touch backend/database/__init__.py

# 6. Backend 테스트
echo ""
echo -e "${YELLOW}6. Backend 테스트${NC}"
echo "-----------------"
cd backend
export PYTHONPATH=.
python -c "
import sys
print('Python 경로:', sys.path[:2])
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
echo ""
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
echo ""
echo -e "${YELLOW}8. Admin 계정 확인${NC}"
echo "------------------"
cd backend
PYTHONPATH=. python create_admin.py 2>/dev/null || echo "Admin 계정이 이미 존재합니다"
cd ..

# 9. Frontend 설정
echo ""
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
if [ -d "node_modules" ]; then
    echo "기존 node_modules를 삭제합니다..."
    rm -rf node_modules package-lock.json
fi
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
    sleep 2
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
echo "========================================================="
echo -e "${GREEN}✅ 시스템 시작 완료!${NC}"
echo "========================================================="
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
