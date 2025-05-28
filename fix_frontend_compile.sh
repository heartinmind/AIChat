#!/bin/bash

# Frontend 컴파일 오류 수정 스크립트

echo "🔧 Frontend 컴파일 오류 수정"
echo "============================"
echo ""

cd /Users/unipurple/Projects/AIChat

# 1. 누락된 패키지 설치
echo "1. 누락된 패키지 설치..."
cd admin
npm install framer-motion jwt-decode@4.0.0 --save

# 2. AuthContext.tsx 수정 (jwt-decode import 방식 변경)
echo ""
echo "2. AuthContext.tsx 파일 수정..."
cd src/contexts

# 백업 생성
cp AuthContext.tsx AuthContext.tsx.backup

# jwt_decode를 jwtDecode로 변경
sed -i '' 's/import jwt_decode from/import { jwtDecode } from/g' AuthContext.tsx
sed -i '' 's/jwt_decode(/jwtDecode(/g' AuthContext.tsx

echo "✅ AuthContext.tsx 수정 완료"

# 3. 변경사항 확인
echo ""
echo "변경된 import 확인:"
grep -n "jwtDecode" AuthContext.tsx | head -5

cd ../../..

echo ""
echo "============================"
echo "✅ 수정 완료!"
echo ""
echo "Frontend가 자동으로 리로드됩니다."
echo "브라우저에서 http://localhost:3001 확인하세요."
echo ""
echo "문제가 지속되면 다음을 확인하세요:"
echo "  tail -f frontend.log"
