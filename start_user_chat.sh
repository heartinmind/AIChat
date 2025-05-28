#!/bin/bash

# 사용자 채팅창 시작 스크립트

echo "🚀 사용자 채팅창 시작"
echo "===================="
echo ""

cd /Users/unipurple/Projects/AIChat

# 1. Backend 상태 확인
echo "1. 시스템 상태 확인..."
if [ -f ".backend.pid" ] && ps -p $(cat .backend.pid) > /dev/null 2>&1; then
    echo "✅ Backend API가 실행 중입니다"
else
    echo "⚠️  Backend API가 실행되지 않았습니다"
    echo "먼저 Backend를 시작해주세요!"
fi

# 2. Frontend 디렉토리로 이동
cd frontend

# 3. node_modules 확인
if [ ! -d "node_modules" ]; then
    echo ""
    echo "2. 패키지 설치..."
    npm install
fi

# 4. 개발 서버 시작
echo ""
echo "3. 사용자 채팅창을 시작합니다..."
echo "포트: 3000 (기본)"
echo ""

# 개발 모드로 시작
npm run dev

# 백그라운드로 실행하려면:
# nohup npm run dev > ../user_chat.log 2>&1 &
# USER_CHAT_PID=$!
# cd ..
# echo $USER_CHAT_PID > .user_chat.pid
# echo "✅ 사용자 채팅창 시작됨 (PID: $USER_CHAT_PID)"
