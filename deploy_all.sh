#!/bin/bash

# Elite Beauty Clinic 배포 스크립트 (개선 버전)

cd /Users/unipurple/Projects/AIChat

echo "🚀 Elite Beauty Clinic 배포 시작!"
echo "================================"
echo ""

# 색상 코드
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 프로젝트 설정
PROJECT_ID="elite-cms-2025"
REGION="asia-northeast3"

# Claude API 키 확인
if [ -f ".env" ]; then
    export $(cat .env | grep CLAUDE_API_KEY | xargs)
fi

if [ -z "$CLAUDE_API_KEY" ]; then
    echo -e "${RED}❌ CLAUDE_API_KEY가 설정되지 않았습니다!${NC}"
    echo "다음 명령어로 설정하세요:"
    echo "export CLAUDE_API_KEY=sk-ant-api..."
    exit 1
fi

echo -e "${GREEN}✅ 환경 설정 완료${NC}"
echo ""

# 1. Backend API 배포
echo -e "${YELLOW}1️⃣ Backend API 배포 중...${NC}"
cd backend

# requirements.txt 링크 생성
if [ ! -f "requirements.txt" ] || [ -L "requirements.txt" ]; then
    rm -f requirements.txt
    ln -s requirements_py313.txt requirements.txt
fi

gcloud run deploy elite-beauty-api \
  --source . \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars "CLAUDE_API_KEY=$CLAUDE_API_KEY,DATABASE_URL=sqlite:///./elite_beauty.db,SECRET_KEY=elite-beauty-secret-key-2024" \
  --memory 512Mi \
  --project $PROJECT_ID \
  --quiet || echo -e "${RED}⚠️  Backend 배포 실패 (계속 진행)${NC}"

echo ""

# 2. Frontend 배포 (오류 시에도 계속 진행)
echo -e "${YELLOW}2️⃣ User Chat 배포 중...${NC}"
cd ../frontend

# package-lock.json 재생성
rm -f package-lock.json
npm install

# 빌드 테스트
echo "빌드 테스트 중..."
npm run build || {
    echo -e "${RED}❌ Frontend 빌드 실패! 문제를 확인하세요.${NC}"
    echo "계속 진행합니다..."
}

# Cloud Run 배포 시도
gcloud run deploy elite-beauty-chat \
  --source . \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --project $PROJECT_ID \
  --quiet || echo -e "${RED}⚠️  Frontend 배포 실패 (계속 진행)${NC}"

echo ""

# 3. Admin Dashboard - Firebase Hosting으로 배포
echo -e "${YELLOW}3️⃣ Admin Dashboard 배포 중 (Firebase Hosting)...${NC}"
cd ../admin

# 환경 변수 설정
export REACT_APP_API_URL="https://elite-beauty-api-asia-northeast3-lm.a.run.app"

# package-lock.json 재생성
rm -f package-lock.json
npm install

# 빌드
echo "Admin Dashboard 빌드 중..."
npm run build

# Firebase 설정 파일 생성
cat > .firebaserc << EOF
{
  "projects": {
    "default": "elite-cms-2025"
  }
}
EOF

# Firebase CLI 설치 확인
if ! command -v firebase &> /dev/null; then
    echo "Firebase CLI 설치 중..."
    npm install -g firebase-tools
fi

# Firebase 배포
echo "Firebase Hosting 배포 중..."
firebase deploy --only hosting --project elite-cms-2025 --non-interactive || {
    echo -e "${RED}⚠️  Firebase 배포 실패. 수동으로 다음 명령어를 실행하세요:${NC}"
    echo "cd admin && firebase login && firebase deploy --only hosting"
}

echo ""

# 배포 정보 출력
echo "================================"
echo -e "${GREEN}🎉 배포 프로세스 완료!${NC}"
echo ""
echo -e "${YELLOW}🌐 접속 URL:${NC}"
echo "- API 문서: https://elite-beauty-api-$REGION-lm.a.run.app/docs"
echo "- 채팅: https://elite-beauty-chat-$REGION-lm.a.run.app"
echo "- 관리자 (Firebase): https://elite-cms-2025.web.app"
echo "  또는: https://elite-cms-2025.firebaseapp.com"
echo ""
echo -e "${YELLOW}👤 관리자 로그인:${NC}"
echo "- 이메일: admin@elitebeauty.com"
echo "- 비밀번호: admin123"
echo ""
echo "================================"
