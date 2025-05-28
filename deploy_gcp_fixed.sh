#!/bin/bash

# GCP Cloud Run 빠른 배포 스크립트

cd /Users/unipurple/Projects/AIChat

echo "🚀 GCP Cloud Run 배포 시작!"
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

# requirements.txt 링크 생성 (py313 버전 사용)
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
  --project $PROJECT_ID

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Backend 배포 실패!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Backend API 배포 완료!${NC}"
echo ""

# 2. Frontend 배포
echo -e "${YELLOW}2️⃣ User Chat 배포 중...${NC}"
cd ../frontend

# package-lock.json 삭제 및 재생성
rm -f package-lock.json
npm install

gcloud run deploy elite-beauty-chat \
  --source . \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --project $PROJECT_ID

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Frontend 배포 실패!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ User Chat 배포 완료!${NC}"
echo ""

# 3. Admin Dashboard 배포
echo -e "${YELLOW}3️⃣ Admin Dashboard 배포 중...${NC}"
cd ../admin

# package-lock.json 삭제 및 재생성
rm -f package-lock.json
npm install

gcloud run deploy elite-beauty-admin \
  --source . \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --project $PROJECT_ID

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Admin 배포 실패!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Admin Dashboard 배포 완료!${NC}"
echo ""

# 배포 정보 출력
echo "================================"
echo -e "${GREEN}🎉 배포가 완료되었습니다!${NC}"
echo ""
echo -e "${YELLOW}🌐 접속 URL:${NC}"
echo "- 채팅: https://elite-beauty-chat-$REGION-lm.a.run.app"
echo "- 관리자: https://elite-beauty-admin-$REGION-lm.a.run.app"
echo "- API 문서: https://elite-beauty-api-$REGION-lm.a.run.app/docs"
echo ""
echo -e "${YELLOW}👤 관리자 로그인:${NC}"
echo "- 이메일: admin@elitebeauty.com"
echo "- 비밀번호: admin123"
echo ""
echo "================================"
