#!/bin/bash

# 빠른 재시작 스크립트

echo "🚀 Elite Beauty Clinic AI 시스템을 재시작합니다..."
echo ""

cd /Users/unipurple/Projects/AIChat

# 프로세스 정리
echo "기존 프로세스 정리..."
pkill -f "python.*main.py" 2>/dev/null
pkill -f "node.*react-scripts" 2>/dev/null
sleep 2

# 가상환경 활성화
source venv/bin/activate

# Backend 시작
echo "Backend 시작..."
cd backend
nohup python main.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Backend 시작 대기
sleep 3

# Backend 상태 확인
if ps -p $BACKEND_PID > /dev/null; then
    echo "✅ Backend 시작됨 (PID: $BACKEND_PID)"
else
    echo "❌ Backend 시작 실패. 로그 확인:"
    tail -10 backend.log
    echo ""
    echo "호환성 문제 해결을 위해 다음을 실행하세요:"
    echo "chmod +x fix_compatibility.sh && ./fix_compatibility.sh"
    exit 1
fi

# Frontend 시작
echo "Frontend 시작..."
cd admin
nohup npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!

# PID 저장
echo $BACKEND_PID > ../.backend.pid
echo $FRONTEND_PID > ../.frontend.pid

echo ""
echo "✅ 시스템이 시작되었습니다!"
echo "📌 접속: http://localhost:3000"
echo "🔑 로그인: admin@elitebeauty.com / admin123"
echo ""
echo "로그 확인: tail -f backend.log"
echo "종료: ./stop_system.sh"
