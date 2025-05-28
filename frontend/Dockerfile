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
