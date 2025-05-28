#!/bin/bash

# 사용자 채팅창 완전 설치 및 실행 스크립트

echo "🚀 사용자 채팅창 완전 설치 및 실행"
echo "=================================="
echo ""

cd /Users/unipurple/Projects/AIChat/frontend

# 1. 필요한 모든 패키지 설치
echo "📦 필요한 패키지를 설치합니다..."
echo ""

npm install --save \
  @heroicons/react \
  uuid \
  @types/uuid

echo ""
echo "✅ 패키지 설치 완료!"
echo ""

# 2. 설치된 패키지 확인
echo "📋 설치된 패키지 확인:"
npm list @heroicons/react uuid

# 3. 환경 변수 설정
echo ""
echo "🔧 환경 설정..."
export PORT=3002
export NEXT_PUBLIC_API_URL=http://localhost:8000

# 4. 개발 서버 시작
echo ""
echo "🌟 사용자 채팅창을 시작합니다..."
echo "=================================="
echo ""
echo "📱 사용자 채팅창: http://localhost:3002"
echo "🔧 관리자 대시보드: http://localhost:3001"
echo "🔌 Backend API: http://localhost:8000"
echo ""
echo "⏳ Next.js가 컴파일 중입니다..."
echo "   브라우저에서 http://localhost:3002 로 접속하세요!"
echo ""

# Next.js 개발 서버 실행
PORT=3002 npm run dev
