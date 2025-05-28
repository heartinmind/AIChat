#!/bin/bash

# Frontend 빠른 수정 스크립트

echo "🚀 Frontend 빠른 수정"
echo "===================="
echo ""

cd /Users/unipurple/Projects/AIChat/admin

# 1. 누락된 ajv 모듈 설치
echo "누락된 ajv 모듈을 설치합니다..."
npm install ajv@8.12.0 --save

# 2. Frontend 재시작
echo ""
echo "Frontend를 재시작합니다..."
pkill -f "react-scripts start" 2>/dev/null
rm -f ../.frontend.pid
sleep 2

PORT=3001 nohup npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!

cd ..
echo $FRONTEND_PID > .frontend.pid

# 3. 시작 확인
echo ""
echo "Frontend 시작 확인 중..."
sleep 5

# 로그 확인
echo ""
echo "최근 로그:"
tail -10 frontend.log

echo ""
echo "================================"
echo "📌 접속 정보:"
echo "   http://localhost:3001"
echo ""
echo "⏳ React 앱이 시작되는 중입니다..."
echo "   로그 실시간 확인: tail -f frontend.log"
echo "================================"
