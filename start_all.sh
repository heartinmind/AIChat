#!/bin/bash

# 전체 시스템 시작 스크립트

echo "🚀 Elite Beauty Clinic AI Chat System 시작"
echo "=========================================="
echo ""

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. 환경 확인
if [ ! -f .env ]; then
    echo "❌ .env 파일이 없습니다! 먼저 ./setup.sh를 실행하세요."
    exit 1
fi

# 2. 기존 프로세스 정리
echo "🧹 기존 프로세스 정리..."
./stop_all.sh 2>/dev/null

# 3. Backend 시작
echo ""
echo -e "${YELLOW}1. Backend API 시작${NC}"
cd backend
source ../venv/bin/activate
PYTHONPATH=. nohup python main.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..
echo $BACKEND_PID > .backend.pid
echo -e "${GREEN}✓ Backend 시작됨 (PID: $BACKEND_PID)${NC}"

# 4. Admin Dashboard 시작
echo ""
echo -e "${YELLOW}2. Admin Dashboard 시작${NC}"
cd admin
PORT=3001 nohup npm start > ../admin.log 2>&1 &
ADMIN_PID=$!
cd ..
echo $ADMIN_PID > .admin.pid
echo -e "${GREEN}✓ Admin Dashboard 시작됨 (PID: $ADMIN_PID)${NC}"

# 5. User Chat 시작
echo ""
echo -e "${YELLOW}3. User Chat Interface 시작${NC}"
cd frontend
PORT=3002 nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo $FRONTEND_PID > .frontend.pid
echo -e "${GREEN}✓ User Chat 시작됨 (PID: $FRONTEND_PID)${NC}"

# 6. 시작 완료
echo ""
echo "=========================================="
echo -e "${GREEN}✅ 모든 서비스가 시작되었습니다!${NC}"
echo "=========================================="
echo ""
echo "📌 접속 URL:"
echo "   • 사용자 채팅: http://localhost:3002"
echo "   • 관리자 대시보드: http://localhost:3001"
echo "   • API 문서: http://localhost:8000/docs"
echo ""
echo "📊 로그 확인:"
echo "   • Backend: tail -f backend.log"
echo "   • Admin: tail -f admin.log"
echo "   • Frontend: tail -f frontend.log"
echo ""
echo "🛑 종료하려면: ./stop_all.sh"
