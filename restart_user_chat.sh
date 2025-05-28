#!/bin/bash

# 사용자 채팅창 재시작 스크립트

echo "🔄 사용자 채팅창 재시작"
echo "====================="
echo ""

# 1. 기존 프로세스 종료
echo "1. 기존 Next.js 프로세스 종료..."

# 포트 3002를 사용하는 프로세스 종료
PORT_PID=$(lsof -ti :3002)
if [ ! -z "$PORT_PID" ]; then
    echo "포트 3002를 사용 중인 프로세스 발견 (PID: $PORT_PID)"
    kill -9 $PORT_PID
    echo "✅ 프로세스 종료됨"
else
    echo "포트 3002가 사용되지 않고 있습니다"
fi

# Next.js 프로세스 종료
pkill -f "next dev" 2>/dev/null

# 잠시 대기
sleep 2

# 2. 프로젝트 디렉토리로 이동
cd /Users/unipurple/Projects/AIChat/frontend

# 3. 개발 서버 재시작
echo ""
echo "2. 사용자 채팅창을 재시작합니다..."
echo "================================"
echo ""
echo "📱 사용자 채팅창: http://localhost:3002"
echo "🔧 관리자 대시보드: http://localhost:3001"
echo "🔌 Backend API: http://localhost:8000"
echo ""

# 환경 변수 설정 및 실행
export PORT=3002
export NEXT_PUBLIC_API_URL=http://localhost:8000

npm run dev
