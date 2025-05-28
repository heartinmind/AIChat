#!/bin/bash

# Frontend 빌드 문제 디버깅 및 수정

cd /Users/unipurple/Projects/AIChat/frontend

echo "🔍 Frontend 빌드 문제 진단 중..."
echo "================================"

# 1. node_modules 삭제 및 재설치
echo "1️⃣ 의존성 정리 중..."
rm -rf node_modules package-lock.json
npm cache clean --force

# 2. 필요한 의존성 확인 및 설치
echo "2️⃣ 의존성 재설치 중..."
npm install

# 3. TypeScript 타입 체크
echo "3️⃣ TypeScript 타입 체크..."
npm run type-check || echo "타입 체크 오류 발견"

# 4. 로컬 빌드 테스트
echo "4️⃣ 로컬 빌드 테스트..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ 로컬 빌드 성공!"
else
    echo "❌ 로컬 빌드 실패!"
    echo ""
    echo "일반적인 문제 해결 방법:"
    echo "1. 모듈 import 경로 확인"
    echo "2. TypeScript 타입 오류 수정"
    echo "3. 환경 변수 설정 확인"
fi

echo ""
echo "5️⃣ Dockerfile 최적화..."

# Dockerfile 재작성 (더 안정적인 버전)
cat > Dockerfile << 'EOF'
FROM node:18-alpine AS deps
# 의존성만 먼저 설치 (캐시 활용)
WORKDIR /app
COPY package.json ./
RUN npm install --legacy-peer-deps

FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# 환경 변수 설정
ENV NEXT_PUBLIC_API_URL=https://elite-beauty-api-asia-northeast3-lm.a.run.app
ENV NODE_ENV=production

# 빌드
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=8080

# 필요한 파일만 복사
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 8080

# Next.js 서버 실행
CMD ["npm", "start"]
EOF

echo "✅ Dockerfile 업데이트 완료!"
echo ""
echo "6️⃣ .gcloudignore 생성..."

cat > .gcloudignore << 'EOF'
# Git
.git
.gitignore

# Dependencies
node_modules/
.next/cache/

# Test files
*.test.js
*.spec.js
coverage/
.nyc_output/

# Development files
.env.local
.env.development

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Misc
.vercel
*.md
!README.md
EOF

echo "✅ 모든 수정 완료!"
echo ""
echo "다음 명령어로 재배포를 시도하세요:"
echo "gcloud run deploy elite-beauty-chat --source . --region asia-northeast3 --allow-unauthenticated --memory 512Mi --project elite-cms-2025"
