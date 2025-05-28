#!/bin/bash

# Ngrok을 사용한 빠른 배포 스크립트

echo "🌐 Ngrok을 사용한 빠른 배포"
echo "============================"
echo ""

# 1. Ngrok 설치 확인
if ! command -v ngrok &> /dev/null; then
    echo "❌ Ngrok이 설치되지 않았습니다!"
    echo ""
    echo "설치 방법:"
    echo "  brew install ngrok"
    echo "  또는"
    echo "  https://ngrok.com/download"
    exit 1
fi

echo "✅ Ngrok 설치 확인됨"
echo ""

# 2. 서비스 확인
echo "📋 실행 중인 서비스 확인:"
echo "------------------------"

if lsof -i :8000 > /dev/null 2>&1; then
    echo "✅ Backend API (포트 8000) - 실행 중"
else
    echo "❌ Backend API (포트 8000) - 실행되지 않음"
    echo "   실행: cd backend && PYTHONPATH=. python main.py"
fi

if lsof -i :3001 > /dev/null 2>&1; then
    echo "✅ Admin Dashboard (포트 3001) - 실행 중"
else
    echo "❌ Admin Dashboard (포트 3001) - 실행되지 않음"
    echo "   실행: cd admin && PORT=3001 npm start"
fi

if lsof -i :3002 > /dev/null 2>&1; then
    echo "✅ User Chat (포트 3002) - 실행 중"
else
    echo "❌ User Chat (포트 3002) - 실행되지 않음"
    echo "   실행: cd frontend && PORT=3002 npm run dev"
fi

echo ""
echo "🚀 Ngrok 실행 명령어:"
echo "--------------------"
echo ""
echo "각각 다른 터미널에서 실행하세요:"
echo ""
echo "# 터미널 1 - Backend API"
echo "ngrok http 8000"
echo ""
echo "# 터미널 2 - Admin Dashboard"
echo "ngrok http 3001"
echo ""
echo "# 터미널 3 - User Chat"
echo "ngrok http 3002"
echo ""
echo "📌 생성된 URL을 팀원들에게 공유하세요!"
echo ""
echo "⚠️  주의사항:"
echo "1. Frontend 환경변수를 ngrok URL로 업데이트 필요"
echo "2. CORS 설정 확인 필요"
echo "3. 무료 버전은 URL이 변경됨"
