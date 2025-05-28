#!/bin/bash

# Frontend 시작 스크립트

echo "🚀 Frontend 시작 스크립트"
echo "========================"
echo ""

cd /Users/unipurple/Projects/AIChat

# 1. 프로세스 상태 확인
echo "현재 실행 중인 서비스 확인..."
if [ -f ".backend.pid" ] && ps -p $(cat .backend.pid) > /dev/null 2>&1; then
    echo "✅ Backend가 실행 중입니다 (PID: $(cat .backend.pid))"
else
    echo "⚠️  Backend가 실행되지 않았습니다"
fi

if [ -f ".frontend.pid" ] && ps -p $(cat .frontend.pid) > /dev/null 2>&1; then
    echo "⚠️  Frontend가 이미 실행 중입니다 (PID: $(cat .frontend.pid))"
    echo "재시작하려면 먼저 ./stop_system.sh를 실행하세요"
    exit 1
fi

# 2. Frontend 디렉토리로 이동
cd admin

# 3. node_modules 확인
if [ ! -d "node_modules" ]; then
    echo ""
    echo "node_modules가 없습니다. 패키지를 설치합니다..."
    npm install --legacy-peer-deps
fi

# 4. Frontend 시작
echo ""
echo "Frontend를 시작합니다..."
nohup npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!

# 5. PID 저장
cd ..
echo $FRONTEND_PID > .frontend.pid

# 6. 시작 확인
echo ""
echo "Frontend 시작을 확인 중..."
sleep 5

if ps -p $FRONTEND_PID > /dev/null; then
    echo "✅ Frontend 시작됨 (PID: $FRONTEND_PID)"
    echo ""
    echo "========================"
    echo "✨ 시스템이 준비되었습니다!"
    echo "========================"
    echo ""
    echo "📌 접속 정보:"
    echo "   Admin Dashboard: http://localhost:3000"
    echo "   Backend API: http://localhost:8000"
    echo "   API 문서: http://localhost:8000/docs"
    echo ""
    echo "🔑 로그인 정보:"
    echo "   이메일: admin@elitebeauty.com"
    echo "   비밀번호: admin123"
    echo ""
    echo "📋 로그 확인:"
    echo "   Frontend: tail -f frontend.log"
    echo "   Backend: tail -f backend.log"
    echo ""
    echo "⏳ React 앱이 시작되는 중입니다..."
    echo "   브라우저가 자동으로 열리거나 http://localhost:3000으로 접속하세요"
else
    echo "❌ Frontend 시작 실패"
    echo "로그 확인:"
    tail -20 frontend.log
fi
