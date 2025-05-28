# 서버 배포 가이드

## 🚀 빠른 배포 (Ngrok 사용 - 임시 테스트용)

### 1. Ngrok 설치
```bash
# Mac
brew install ngrok

# 또는 https://ngrok.com 에서 다운로드
```

### 2. Ngrok 실행
```bash
# 터미널 1: Backend API 노출
ngrok http 8000

# 터미널 2: Admin Dashboard 노출  
ngrok http 3001

# 터미널 3: User Chat 노출
ngrok http 3002
```

### 3. 환경 변수 업데이트
Frontend의 API URL을 ngrok URL로 변경:
```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=https://your-ngrok-url.ngrok.io

# admin/src/contexts/AuthContext.tsx
const API_BASE_URL = 'https://your-ngrok-url.ngrok.io';
```

## 🏢 프로덕션 배포 (AWS/GCP)

### AWS EC2 배포

#### 1. EC2 인스턴스 생성
- Ubuntu 22.04 LTS
- t3.medium 이상 권장
- 보안 그룹: 80, 443, 8000, 3001, 3002 포트 열기

#### 2. 서버 설정
```bash
# 서버 접속 후
sudo apt update
sudo apt install python3.12 python3.12-venv nginx nodejs npm

# 프로젝트 클론
git clone https://github.com/YOUR_REPO.git
cd YOUR_REPO

# 설정 실행
./setup.sh
```

#### 3. Nginx 설정
```nginx
# /etc/nginx/sites-available/elitebeauty
server {
    listen 80;
    server_name your-domain.com;

    # User Chat
    location / {
        proxy_pass http://localhost:3002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Admin Dashboard
    location /admin {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

#### 4. SSL 설정 (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

#### 5. PM2로 프로세스 관리
```bash
npm install -g pm2

# ecosystem.config.js 생성
module.exports = {
  apps: [
    {
      name: 'backend',
      script: 'python',
      args: 'main.py',
      cwd: './backend',
      interpreter: './venv/bin/python',
      env: {
        PYTHONPATH: '.'
      }
    },
    {
      name: 'admin',
      script: 'npm',
      args: 'start',
      cwd: './admin',
      env: {
        PORT: 3001
      }
    },
    {
      name: 'frontend',
      script: 'npm',
      args: 'start',
      cwd: './frontend',
      env: {
        PORT: 3002
      }
    }
  ]
}

# 실행
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

### Docker 배포

#### Docker Compose 설정
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - CLAUDE_API_KEY=${CLAUDE_API_KEY}
      - DATABASE_URL=sqlite:///./elite_beauty.db
    volumes:
      - ./backend/elite_beauty.db:/app/elite_beauty.db

  admin:
    build: ./admin
    ports:
      - "3001:3001"
    environment:
      - REACT_APP_API_URL=http://backend:8000
    depends_on:
      - backend

  frontend:
    build: ./frontend
    ports:
      - "3002:3002"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - admin
      - frontend
```

## 🔒 보안 고려사항

1. **환경 변수**
   - 모든 민감한 정보는 환경 변수로
   - .env 파일은 절대 커밋하지 않기

2. **HTTPS 필수**
   - 프로덕션에서는 반드시 SSL 인증서 사용

3. **방화벽 설정**
   - 필요한 포트만 열기
   - IP 화이트리스트 고려

4. **정기 백업**
   - 데이터베이스 정기 백업
   - 로그 파일 관리

## 📊 모니터링

1. **로그 수집**
   - CloudWatch (AWS)
   - Stackdriver (GCP)
   - ELK Stack

2. **성능 모니터링**
   - New Relic
   - Datadog
   - Prometheus + Grafana

3. **에러 추적**
   - Sentry
   - Rollbar
