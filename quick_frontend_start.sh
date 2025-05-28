#!/bin/bash

# Frontend 시작 스크립트

echo "🎨 Frontend 시작"
echo "==============="
echo ""

cd /Users/unipurple/Projects/AIChat/admin

# 1. node_modules 확인
if [ ! -d "node_modules" ]; then
    echo "node_modules가 없습니다. 패키지를 설치합니다..."
    npm install --legacy-peer-deps
fi

# 2. 프로세스 정리
echo "기존 Frontend 프로세스 정리..."
pkill -f "node.*react-scripts" 2>/dev/null
rm -f ../.frontend.pid
sleep 1

# 3. Frontend 시작
echo ""
echo "Frontend를 시작합니다..."
echo "========================"
npm start

# 백그라운드로 실행하려면:
# nohup npm start > ../frontend.log 2>&1 &
# FRONTEND_PID=$!
# echo $FRONTEND_PID > ../.frontend.pid
# echo "✅ Frontend 시작됨 (PID: $FRONTEND_PID)"
