#!/bin/bash

# 다른 포트로 Frontend 시작 스크립트

echo "🚀 Frontend 시작 (포트 3001)"
echo "============================"
echo ""

cd /Users/unipurple/Projects/AIChat

# 1. Backend 상태 확인
if [ -f ".backend.pid" ] && ps -p $(cat .backend.pid) > /dev/null 2>&1; then
    echo "✅ Backend가 실행 중입니다"
else
    echo "⚠️  Backend가 실행되지 않았습니다"
fi

# 2. Frontend 시작 (포트 3001)
echo ""
echo "Frontend를 포트 3001에서 시작합니다..."
cd admin

# PORT 환경변수를 3001로 설정
PORT=3001 nohup npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!

cd ..
echo $FRONTEND_PID > .frontend.pid

# 3. 시작 확인
sleep 5

if ps -p $FRONTEND_PID > /dev/null; then
    echo ""
    echo "✅ Frontend 시작됨 (PID: $FRONTEND_PID)"
    echo ""
    echo "============================"
    echo "✨ 시스템이 준비되었습니다!"
    echo "============================"
    echo ""
    echo "📌 접속 정보:"
    echo "   Admin Dashboard: http://localhost:3001  ⬅️ 포트 변경됨!"
    echo "   Backend API: http://localhost:8000"
    echo "   API 문서: http://localhost:8000/docs"
    echo ""
    echo "🔑 로그인 정보:"
    echo "   이메일: admin@elitebeauty.com"
    echo "   비밀번호: admin123"
    echo ""
    echo "⏳ React 앱이 로딩 중입니다..."
    echo "   브라우저에서 http://localhost:3001로 접속하세요"
else
    echo "❌ Frontend 시작 실패"
    tail -20 frontend.log
fi
