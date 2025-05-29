#!/bin/bash

# Frontend 수정사항 적용 및 재빌드

cd /Users/unipurple/Projects/AIChat/frontend

echo "🔧 Frontend 구조 수정 완료!"
echo "========================="
echo ""
echo "✅ 페이지 구조 정리:"
echo "  - / → 랜딩페이지 (로그인)"
echo "  - /chat → 채팅 페이지"
echo ""

# 의존성 재설치
echo "📦 의존성 재설치 중..."
rm -rf node_modules package-lock.json
npm install

# 빌드 테스트
echo ""
echo "🏗️ 빌드 테스트..."
npm run build

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 빌드 성공!"
    echo ""
    echo "다음 단계:"
    echo "1. git add -A"
    echo "2. git commit -m 'fix: Restructure pages and fix routing paths'"
    echo "3. git push"
    echo "4. ./deploy_all.sh 실행"
else
    echo ""
    echo "❌ 빌드 실패!"
fi
