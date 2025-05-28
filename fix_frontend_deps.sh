#!/bin/bash

# Frontend 의존성 문제 해결 스크립트

echo "🔧 Frontend 의존성 문제 해결"
echo "==========================="
echo ""

cd /Users/unipurple/Projects/AIChat/admin

# 1. 기존 node_modules와 lock 파일 삭제
echo "기존 패키지 정리..."
rm -rf node_modules package-lock.json

# 2. npm 캐시 정리
echo "npm 캐시 정리..."
npm cache clean --force

# 3. ajv 관련 패키지 명시적 설치
echo ""
echo "필수 패키지 설치..."
npm install ajv@8.12.0 ajv-keywords@5.1.0 --save

# 4. 전체 패키지 재설치
echo ""
echo "전체 패키지 설치 (legacy-peer-deps 옵션 사용)..."
npm install --legacy-peer-deps

# 5. Frontend 재시작
echo ""
echo "Frontend를 포트 3001에서 재시작합니다..."
pkill -f "npm start" 2>/dev/null
sleep 2

PORT=3001 nohup npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!

cd ..
echo $FRONTEND_PID > .frontend.pid

# 6. 시작 확인
echo ""
echo "시작 확인 중..."
sleep 10

if ps -p $FRONTEND_PID > /dev/null; then
    echo "✅ Frontend 프로세스 시작됨 (PID: $FRONTEND_PID)"
    echo ""
    echo "⏳ React 앱이 컴파일 중입니다..."
    echo "   약 30-60초 후 http://localhost:3001 로 접속하세요"
    echo ""
    echo "📋 로그 확인: tail -f frontend.log"
else
    echo "❌ Frontend 시작 실패"
    echo "최근 로그:"
    tail -20 frontend.log
fi
