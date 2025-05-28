#!/bin/bash

# 빠른 GCP Cloud Run 배포

cd /Users/unipurple/Projects/AIChat

echo "🚀 GCP Cloud Run 빠른 배포 시작!"
echo ""

# 환경 변수 확인
if [ -z "$CLAUDE_API_KEY" ]; then
    echo "⚠️  CLAUDE_API_KEY를 .env 파일에서 복사해주세요:"
    echo "cat .env | grep CLAUDE_API_KEY"
    echo ""
    echo "export CLAUDE_API_KEY=sk-ant-api..."
    exit 1
fi

# 1. Backend 배포
echo "1️⃣ Backend API 배포 중..."
cd backend
gcloud run deploy elite-beauty-api \
  --source . \
  --region asia-northeast3 \
  --allow-unauthenticated \
  --set-env-vars CLAUDE_API_KEY=$CLAUDE_API_KEY \
  --project elite-cms-2025

# 2. Frontend 환경변수 업데이트
cd ../frontend
echo "NEXT_PUBLIC_API_URL=https://elite-beauty-api-asia-northeast3-lm.a.run.app" > .env.production

# 3. Frontend 배포
echo "2️⃣ User Chat 배포 중..."
gcloud run deploy elite-beauty-chat \
  --source . \
  --region asia-northeast3 \
  --allow-unauthenticated \
  --project elite-cms-2025

# 4. Admin 환경변수 업데이트
cd ../admin
sed -i '' 's|http://localhost:8000|https://elite-beauty-api-asia-northeast3-lm.a.run.app|g' src/contexts/AuthContext.tsx

# 5. Admin 배포
echo "3️⃣ Admin Dashboard 배포 중..."
gcloud run deploy elite-beauty-admin \
  --source . \
  --region asia-northeast3 \
  --allow-unauthenticated \
  --project elite-cms-2025

echo ""
echo "✅ 배포 완료!"
echo ""
echo "🌐 접속 URL:"
echo "- 채팅: https://elite-beauty-chat-asia-northeast3-lm.a.run.app"
echo "- 관리자: https://elite-beauty-admin-asia-northeast3-lm.a.run.app"
echo "- API 문서: https://elite-beauty-api-asia-northeast3-lm.a.run.app/docs"
echo ""
echo "👤 관리자 로그인:"
echo "- 이메일: admin@elitebeauty.com"
echo "- 비밀번호: admin123"
