FROM node:18-alpine AS builder

WORKDIR /app

# 의존성 파일 복사
COPY package*.json ./

# 의존성 설치
RUN npm ci

# 소스 코드 복사
COPY . .

# 환경 변수 설정 (빌드 시)
ENV NEXT_PUBLIC_API_URL=https://elite-beauty-api-asia-northeast3-lm.a.run.app

# 빌드
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# 필요한 파일만 복사
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules

# PORT 환경 변수
ENV PORT=8080
ENV NODE_ENV=production

# Next.js 서버 실행
CMD ["npm", "start"]
