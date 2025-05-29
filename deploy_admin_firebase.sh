#!/bin/bash

# Admin Firebase 수동 배포

echo "🔥 Admin Dashboard - Firebase Hosting 배포"
echo "========================================"
echo ""

PROJECT_ID="elite-cms-2025"
cd /Users/unipurple/Projects/AIChat/admin

# 1. 빌드
echo "1️⃣ Admin 빌드 중..."
export REACT_APP_API_URL="https://elite-beauty-api-asia-northeast3-lm.a.run.app"
npm run build

if [ $? -ne 0 ]; then
    echo "❌ 빌드 실패!"
    exit 1
fi

echo "✅ 빌드 성공!"
echo ""

# 2. Firebase 설정 확인
echo "2️⃣ Firebase 설정 확인..."
if [ ! -f "firebase.json" ]; then
    echo "firebase.json이 없습니다. 생성합니다..."
    cat > firebase.json << 'EOF'
{
  "hosting": {
    "public": "build",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
EOF
fi

if [ ! -f ".firebaserc" ]; then
    echo ".firebaserc가 없습니다. 생성합니다..."
    cat > .firebaserc << EOF
{
  "projects": {
    "default": "$PROJECT_ID"
  }
}
EOF
fi

# 3. Firebase 배포
echo ""
echo "3️⃣ Firebase 배포 시작..."
echo ""
echo "다음 명령어를 수동으로 실행하세요:"
echo ""
echo "1. Firebase 로그인 (처음인 경우):"
echo "   firebase login"
echo ""
echo "2. Firebase 배포:"
echo "   firebase deploy --only hosting --project $PROJECT_ID"
echo ""
echo "또는 이미 로그인되어 있다면:"
firebase deploy --only hosting --project $PROJECT_ID

echo ""
echo "✅ 배포 완료 후 접속 URL:"
echo "- https://$PROJECT_ID.web.app"
echo "- https://$PROJECT_ID.firebaseapp.com"
echo ""
echo "👤 관리자 로그인:"
echo "- 이메일: admin@elitebeauty.com"
echo "- 비밀번호: admin123"
