#!/bin/bash

# Frontend 재시작 스크립트

echo "🔄 Frontend 재시작"
echo "=================="
echo ""

cd /Users/unipurple/Projects/AIChat

# 1. 기존 프로세스 종료
echo "기존 Frontend 프로세스 종료..."
pkill -f "react-scripts start" 2>/dev/null
if [ -f ".frontend.pid" ]; then
    kill -9 $(cat .frontend.pid) 2>/dev/null
fi
rm -f .frontend.pid
sleep 2

# 2. node_modules 확인
cd admin
if [ ! -d "node_modules/framer-motion" ]; then
    echo "framer-motion이 설치되지 않았습니다. 재설치합니다..."
    rm -rf node_modules/.cache
    npm install
fi

# 3. TypeScript 캐시 정리
echo "TypeScript 캐시 정리..."
rm -rf node_modules/.cache
rm -rf tsconfig.tsbuildinfo

# 4. Frontend 재시작
echo ""
echo "Frontend를 포트 3001에서 재시작합니다..."
PORT=3001 nohup npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!

cd ..
echo $FRONTEND_PID > .frontend.pid

# 5. 시작 확인
sleep 5
echo ""
if ps -p $FRONTEND_PID > /dev/null; then
    echo "✅ Frontend 프로세스 시작됨 (PID: $FRONTEND_PID)"
    echo ""
    echo "⏳ React 앱이 컴파일 중입니다..."
    echo "   약 30초 후 http://localhost:3001 로 접속하세요"
    echo ""
    echo "📋 실시간 로그 확인:"
    echo "   tail -f frontend.log"
else
    echo "❌ Frontend 시작 실패"
    tail -20 frontend.log
fi
