#!/bin/bash

# GCP Cloud Run 배포 스크립트

echo "🚀 Elite Beauty Clinic AI Chat - GCP 배포"
echo "========================================="
echo ""

PROJECT_ID="elite-cms-2025"
REGION="asia-northeast3"  # 서울 리전

# 색상 코드
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}📋 배포할 서비스:${NC}"
echo "1. Backend API (포트 8000)"
echo "2. Admin Dashboard (포트 3001)"
echo "3. User Chat (포트 3002)"
echo ""

# 1. Google Cloud SDK 확인
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI가 설치되지 않았습니다!${NC}"
    echo "설치: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# 2. 프로젝트 설정
echo -e "${GREEN}✅ GCP 프로젝트 설정...${NC}"
gcloud config set project $PROJECT_ID

# 3. 필요한 API 활성화
echo -e "${GREEN}✅ 필요한 API 활성화...${NC}"
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# 4. Backend Dockerfile 생성
cat > backend/Dockerfile << 'EOF'
FROM python:3.12-slim

WORKDIR /app

COPY requirements_py313.txt .
RUN pip install --no-cache-dir -r requirements_py313.txt

COPY . .

ENV PYTHONPATH=/app
ENV PORT=8080

CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT
EOF

# 5. Frontend Dockerfile 생성
cat > frontend/Dockerfile << 'EOF'
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
ENV NEXT_PUBLIC_API_URL=https://elite-beauty-api-${REGION}-lm.a.run.app
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules

ENV PORT=8080
CMD ["npm", "start"]
EOF

# 6. Admin Dockerfile 생성
cat > admin/Dockerfile << 'EOF'
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
EOF

# Admin nginx.conf
cat > admin/nginx.conf << 'EOF'
server {
    listen 8080;
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
EOF

echo ""
echo -e "${YELLOW}🔧 배포 명령어:${NC}"
echo ""
echo "# 1. Backend 배포"
echo -e "${GREEN}cd backend${NC}"
echo "gcloud run deploy elite-beauty-api \\"
echo "  --source . \\"
echo "  --region $REGION \\"
echo "  --allow-unauthenticated \\"
echo "  --set-env-vars CLAUDE_API_KEY=YOUR_ACTUAL_API_KEY"
echo ""
echo "# 2. Frontend 배포"
echo -e "${GREEN}cd ../frontend${NC}"
echo "gcloud run deploy elite-beauty-chat \\"
echo "  --source . \\"
echo "  --region $REGION \\"
echo "  --allow-unauthenticated"
echo ""
echo "# 3. Admin 배포"
echo -e "${GREEN}cd ../admin${NC}"
echo "# AuthContext.tsx에서 API URL 업데이트 후:"
echo "gcloud run deploy elite-beauty-admin \\"
echo "  --source . \\"
echo "  --region $REGION \\"
echo "  --allow-unauthenticated"
echo ""
echo -e "${YELLOW}📌 배포 후 URL:${NC}"
echo "- API: https://elite-beauty-api-$REGION-lm.a.run.app"
echo "- Chat: https://elite-beauty-chat-$REGION-lm.a.run.app"
echo "- Admin: https://elite-beauty-admin-$REGION-lm.a.run.app"
