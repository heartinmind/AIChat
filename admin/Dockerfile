FROM node:18-alpine AS builder

WORKDIR /app

# 의존성 파일 복사
COPY package*.json ./

# 의존성 설치
RUN npm ci --legacy-peer-deps

# 소스 코드 복사
COPY . .

# 환경 변수 설정 (빌드 시)
ENV REACT_APP_API_URL=https://elite-beauty-api-asia-northeast3-lm.a.run.app

# 빌드
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# serve 패키지 설치
RUN npm install -g serve

# 빌드된 파일 복사
COPY --from=builder /app/build ./build

# PORT 환경 변수 사용
ENV PORT=8080

# serve로 정적 파일 서빙
CMD serve -s build -l ${PORT}
