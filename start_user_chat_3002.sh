#!/bin/bash

# 사용자 채팅창 시작 스크립트 (포트 3002)

echo "🚀 Elite Beauty Clinic 사용자 채팅창 시작"
echo "========================================"
echo ""

cd /Users/unipurple/Projects/AIChat

# 1. Backend 상태 확인
echo "📌 시스템 상태 확인..."
if [ -f ".backend.pid" ] && ps -p $(cat .backend.pid) > /dev/null 2>&1; then
    echo "✅ Backend API: 실행 중 (포트 8000)"
else
    echo "❌ Backend API가 실행되지 않았습니다!"
    echo "   먼저 Backend를 시작해주세요: ./quick_backend_start.sh"
    exit 1
fi

if [ -f ".frontend.pid" ] && ps -p $(cat .frontend.pid) > /dev/null 2>&1; then
    echo "✅ 관리자 대시보드: 실행 중 (포트 3001)"
fi

# 2. Frontend 디렉토리로 이동
cd frontend

# 3. 환경 변수 설정
echo ""
echo "📌 환경 설정..."
export PORT=3002
export NEXT_PUBLIC_API_URL=http://localhost:8000

# 4. node_modules 확인 및 설치
if [ ! -d "node_modules" ]; then
    echo "📦 패키지 설치 중..."
    npm install
fi

# 5. 개발 서버 시작
echo ""
echo "🌟 사용자 채팅창을 시작합니다..."
echo "=================================="
echo ""
echo "📱 사용자 채팅창: http://localhost:3002"
echo "🔧 관리자 대시보드: http://localhost:3001"
echo "🔌 Backend API: http://localhost:8000"
echo ""
echo "⏳ Next.js가 시작되는 중입니다..."
echo "   브라우저에서 http://localhost:3002 로 접속하세요!"
echo ""

# 포트 3002에서 실행
PORT=3002 npm run dev
