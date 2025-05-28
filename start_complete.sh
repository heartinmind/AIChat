#!/bin/bash

# Elite Beauty Clinic AI 상담 시스템 - 완전 자동 실행 스크립트

clear
echo "======================================================"
echo "🏥 Elite Beauty Clinic AI 상담 시스템"
echo "======================================================"
echo ""

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 프로젝트 디렉토리
PROJECT_DIR="/Users/unipurple/Projects/AIChat"
cd "$PROJECT_DIR"

# 1. 기존 프로세스 정리
echo -e "${YELLOW}1. 기존 프로세스 정리 중...${NC}"
pkill -f "python.*main.py" 2>/dev/null
pkill -f "node.*react-scripts" 2>/dev/null
sleep 2
echo -e "${GREEN}✓ 완료${NC}"
echo ""

# 2. Python 환경 설정
echo -e "${YELLOW}2. Python 환경 설정 중...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# pip 업그레이드
pip install --upgrade pip --quiet

# 최소 요구사항 설치
pip install --quiet -r backend/requirements_minimal.txt
echo -e "${GREEN}✓ 완료${NC}"
echo ""

# 3. 환경 파일 생성
echo -e "${YELLOW}3. 환경 설정 중...${NC}"
if [ ! -f ".env" ]; then
    cat > .env << EOL
SECRET_KEY=dev-secret-key-for-elite-beauty-clinic
CLAUDE_API_KEY=sk-ant-api03-YOUR-KEY-HERE
DATABASE_URL=sqlite:///./elite_beauty.db
EOL
fi
echo -e "${GREEN}✓ 완료${NC}"
echo ""

# 4. Admin 계정 생성
echo -e "${YELLOW}4. Admin 계정 생성 중...${NC}"
cd backend
python create_admin.py 2>/dev/null || echo "Admin 계정이 이미 존재합니다."
cd ..
echo -e "${GREEN}✓ 완료${NC}"
echo ""

# 5. Backend 시작
echo -e "${YELLOW}5. Backend 서버 시작 중...${NC}"
cd backend
nohup python main.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Backend 시작 확인
sleep 3
if ps -p $BACKEND_PID > /dev/null; then
    echo -e "${GREEN}✓ Backend 서버가 시작되었습니다 (PID: $BACKEND_PID)${NC}"
else
    echo -e "${RED}✗ Backend 서버 시작 실패${NC}"
    echo "로그 확인: tail -f backend.log"
    exit 1
fi
echo ""

# 6. Frontend 설정
echo -e "${YELLOW}6. Frontend 설정 중...${NC}"
cd admin

# 패키지 설치
if [ ! -d "node_modules" ]; then
    echo "패키지 설치 중... (약 1-2분 소요)"
    rm -f package-lock.json
    npm install --legacy-peer-deps > ../npm_install.log 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 패키지 설치 완료${NC}"
    else
        echo -e "${RED}✗ 패키지 설치 실패${NC}"
        echo "로그 확인: cat ../npm_install.log"
        exit 1
    fi
else
    echo -e "${GREEN}✓ 패키지가 이미 설치되어 있습니다${NC}"
fi
echo ""

# 7. Frontend 시작
echo -e "${YELLOW}7. Frontend 시작 중...${NC}"
nohup npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!

# Frontend 시작 확인
sleep 5
if ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${GREEN}✓ Frontend가 시작되었습니다 (PID: $FRONTEND_PID)${NC}"
else
    echo -e "${RED}✗ Frontend 시작 실패${NC}"
    echo "로그 확인: tail -f frontend.log"
    exit 1
fi
echo ""

# 8. 시스템 상태 확인
echo -e "${YELLOW}8. 시스템 상태 확인 중...${NC}"
sleep 3

# Backend 확인
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✓ Backend API 정상 작동${NC}"
else
    echo -e "${RED}✗ Backend API 응답 없음${NC}"
fi

# Frontend 확인
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Admin Dashboard 정상 작동${NC}"
else
    echo -e "${YELLOW}! Admin Dashboard 시작 중... (잠시만 기다려주세요)${NC}"
fi
echo ""

# 완료 메시지
echo "======================================================"
echo -e "${GREEN}✅ 시스템이 성공적으로 시작되었습니다!${NC}"
echo "======================================================"
echo ""
echo "📌 접속 정보:"
echo "   Admin Dashboard: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API 문서: http://localhost:8000/docs"
echo ""
echo "👤 로그인 정보:"
echo "   이메일: admin@elitebeauty.com"
echo "   비밀번호: admin123"
echo ""
echo "📋 유용한 명령어:"
echo "   로그 확인: tail -f backend.log"
echo "   상태 확인: ./check_status.sh"
echo "   시스템 종료: ./stop_system.sh"
echo ""
echo "🌐 브라우저가 자동으로 열리지 않으면"
echo "   직접 http://localhost:3000 으로 접속하세요"
echo ""
echo "======================================================"
echo ""

# PID 파일 저장
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

# 로그 모니터링 옵션
echo -n "로그를 실시간으로 보시겠습니까? (y/N): "
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "Backend 로그를 표시합니다. (종료: Ctrl+C)"
    tail -f backend.log
fi
