#!/bin/bash

# 사용자 채팅창 재시작 스크립트

echo "🔄 사용자 채팅창 재시작"
echo "====================="
echo ""

cd /Users/unipurple/Projects/AIChat

# 1. 기존 프로세스 종료
echo "기존 프로세스 종료..."
pkill -f "next dev" 2>/dev/null
lsof -ti :3002 | xargs kill -9 2>/dev/null
sleep 2

# 2. Frontend 디렉토리로 이동
cd frontend

# 3. 환경 변수 설정
export PORT=3002
export NEXT_PUBLIC_API_URL=http://localhost:8000

# 4. 개발 서버 시작
echo ""
echo "사용자 채팅창을 재시작합니다..."
echo "=============================="
echo ""
echo "📱 사용자 채팅창: http://localhost:3002"
echo "🔧 관리자 대시보드: http://localhost:3001"
echo "🔌 Backend API: http://localhost:8000"
echo ""

npm run dev
