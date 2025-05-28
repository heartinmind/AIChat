#!/bin/bash

# 사용자 채팅창 의존성 수정 스크립트

echo "🔧 사용자 채팅창 의존성 문제 해결"
echo "================================"
echo ""

cd /Users/unipurple/Projects/AIChat/frontend

# 1. 누락된 패키지 설치
echo "1. 누락된 패키지 설치..."
npm install @heroicons/react --save

# 2. 기타 필요할 수 있는 패키지 확인 및 설치
echo ""
echo "2. 추가 패키지 설치..."
npm install --save \
  @heroicons/react \
  clsx \
  react-icons

# 3. node_modules 정리 (필요시)
if [ -d "node_modules/.cache" ]; then
    echo ""
    echo "3. 캐시 정리..."
    rm -rf node_modules/.cache
fi

# 4. 개발 서버 재시작
echo ""
echo "4. 사용자 채팅창을 포트 3002에서 시작합니다..."
echo "============================================"
echo ""
echo "📱 사용자 채팅창: http://localhost:3002"
echo ""

# 포트 3002에서 실행
PORT=3002 npm run dev
