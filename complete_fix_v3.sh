#!/bin/bash

# Elite Beauty Clinic AI 시스템 - Python 3.13 호환 버전

echo "🔧 Elite Beauty Clinic AI 시스템 문제 해결을 시작합니다 (v3 - Python 3.13 호환)..."
echo "=================================================================="
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
PYTHON_VERSION=""
for py in python3.13 python3.12 python3.11 python3.10 python3.9 python3 python; do
    if command -v $py &> /dev/null; then
        VERSION=$($py -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        echo -e "${GREEN}✓ $py 발견: $(which $py) (버전: $VERSION)${NC}"
        PYTHON_CMD=$py
        PYTHON_VERSION=$VERSION
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo -e "${RED}❌ Python이 설치되지 않았습니다!${NC}"
    echo "Homebrew로 설치: brew install python@3.12"
    exit 1
fi

echo ""
echo -e "${GREEN}사용할 Python: $PYTHON_CMD (버전: $PYTHON_VERSION)${NC}"

# Python 버전에 따른 requirements 파일 선택
if [[ "$PYTHON_VERSION" == "3.13" ]]; then
    echo -e "${YELLOW}Python 3.13 감지 - 최신 호환 패키지를 사용합니다${NC}"
    REQUIREMENTS_FILE="backend/requirements_py313.txt"
else
    echo -e "${GREEN}Python $PYTHON_VERSION 감지 - 안정 버전 패키지를 사용합니다${NC}"
    REQUIREMENTS_FILE="backend/requirements_fixed.txt"
fi

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
    exit 1
fi

echo -e "${GREEN}✓ 가상환경 생성 성공${NC}"

# 가상환경 활성화
echo "가상환경을 활성화합니다..."
source venv/bin/activate

# Python과 pip 경로 확인
echo "Python 경로: $(which python)"
echo "pip 경로: $(which pip)"

# pip 업그레이드 및 wheel 설치
echo ""
echo "pip를 업그레이드하고 wheel을 설치합니다..."
python -m pip install --upgrade pip wheel setuptools

# 4. Backend 패키지 설치
echo ""
echo -e "${YELLOW}4. Backend 패키지 설치${NC}"
echo "----------------------"

# Python 3.13의 경우 특별 처리
if [[ "$PYTHON_VERSION" == "3.13" ]]; then
    echo -e "${YELLOW}Python 3.13용 특별 설치 프로세스를 시작합니다...${NC}"
    
    # pre-built wheel 우선 시도
    echo "Pre-built wheel 패키지 설치 시도..."
    pip install --only-binary :all: pydantic pydantic-core 2>/dev/null || true
    
    # requirements 파일로 설치
    echo "전체 패키지를 설치합니다..."
    pip install -r $REQUIREMENTS_FILE --prefer-binary
    
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}일부 패키지 설치 실패. 핵심 패키지만 설치합니다...${NC}"
        # 최소 필수 패키지만 설치
        pip install fastapi uvicorn[standard] sqlalchemy anthropic httpx python-jose[cryptography] passlib[bcrypt] python-dotenv loguru
    fi
else
    # Python 3.12 이하 버전
    echo "패키지를 설치합니다..."
    pip install -r $REQUIREMENTS_FILE
fi

# 5. database.models 문제 해결
echo ""
echo -e "${YELLOW}5. Database 모듈 설정${NC}"
echo "----------------------"

# __init__.py 파일 확인 및 생성
touch backend/__init__.py
touch backend/database/__init__.py

# 6. Backend 테스트
echo ""
echo -e "${YELLOW}6. Backend 테스트${NC}"
echo "-----------------"
cd backend
export PYTHONPATH=.

# Python 3.13의 경우 특별한 테스트
if [[ "$PYTHON_VERSION" == "3.13" ]]; then
    echo -e "${YELLOW}Python 3.13 호환성 테스트...${NC}"
    python -c "
import sys
print(f'Python 버전: {sys.version}')
print('설치된 패키지 확인:')
try:
    import pydantic
    print(f'  ✓ pydantic: {pydantic.__version__}')
except Exception as e:
    print(f'  ✗ pydantic: {e}')
try:
    import fastapi
    print(f'  ✓ fastapi: {fastapi.__version__}')
except Exception as e:
    print(f'  ✗ fastapi: {e}')
try:
    import sqlalchemy
    print(f'  ✓ sqlalchemy: {sqlalchemy.__version__}')
except Exception as e:
    print(f'  ✗ sqlalchemy: {e}')
"
fi

# 일반 테스트
python -c "
import sys
sys.path.insert(0, '.')
print('')
print('모듈 임포트 테스트:')
try:
    from database.models import Base
    print('  ✓ database.models import 성공!')
except Exception as e:
    print(f'  ✗ database.models import 실패: {e}')
try:
    from main import app
    print('  ✓ main.py import 성공!')
    print('')
    print('✅ Backend 준비 완료!')
except Exception as e:
    print(f'  ✗ main.py import 실패: {e}')
" || true

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
PYTHONPATH=. python create_admin.py 2>/dev/null || echo "Admin 계정이 이미 존재하거나 생성 중 오류 발생"
cd ..

# 9. Frontend 설정 (간략히)
echo ""
echo -e "${YELLOW}9. Frontend 설정${NC}"
echo "-----------------"
if [ ! -d "admin/node_modules" ]; then
    cd admin
    npm install --legacy-peer-deps
    cd ..
else
    echo -e "${GREEN}✓ Frontend 패키지가 이미 설치되어 있습니다${NC}"
fi

# 10. 시스템 시작
echo ""
echo -e "${YELLOW}10. 시스템 시작${NC}"
echo "----------------"

# Backend 시작 시도
echo "Backend를 시작합니다..."
cd backend
PYTHONPATH=. python main.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Backend 시작 확인
sleep 3
if ps -p $BACKEND_PID > /dev/null; then
    echo -e "${GREEN}✓ Backend 프로세스 시작됨 (PID: $BACKEND_PID)${NC}"
    
    # API 상태 확인
    sleep 2
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend API 정상 작동${NC}"
    else
        echo -e "${YELLOW}! Backend API 응답 대기 중...${NC}"
    fi
else
    echo -e "${RED}✗ Backend 시작 실패${NC}"
    echo "최근 로그:"
    tail -20 backend.log
    echo ""
    echo -e "${YELLOW}💡 Python 3.13 호환성 문제일 수 있습니다.${NC}"
    echo "다음을 시도해보세요:"
    echo "1. Python 3.12 설치: brew install python@3.12"
    echo "2. Python 3.12로 가상환경 재생성:"
    echo "   python3.12 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r backend/requirements_fixed.txt"
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
echo "=================================================================="
echo -e "${GREEN}✅ 시스템 시작 완료!${NC}"
echo "=================================================================="
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
echo ""
echo -e "${YELLOW}⚠️  Python 3.13 관련 참고사항:${NC}"
echo "Python 3.13은 매우 최신 버전이라 일부 패키지 호환성 문제가 있을 수 있습니다."
echo "문제가 지속되면 Python 3.12 사용을 권장합니다."
