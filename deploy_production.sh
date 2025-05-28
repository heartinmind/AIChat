#!/bin/bash

# Production 서버 배포 스크립트

echo "🚀 Production 서버 배포 가이드"
echo "==============================="
echo ""

# 1. 서버 준비사항
echo "📋 서버 준비사항:"
echo "- Ubuntu 20.04/22.04 LTS"
echo "- 최소 2GB RAM"
echo "- 포트: 80, 443, 8000, 3001, 3002"
echo ""

# 2. 서버 접속 후 실행할 명령어
cat << 'EOF' > server_setup.sh
#!/bin/bash

# 서버 업데이트
sudo apt update && sudo apt upgrade -y

# 필요한 패키지 설치
sudo apt install -y python3.12 python3.12-venv python3-pip nodejs npm nginx certbot python3-certbot-nginx

# Git 클론
git clone https://github.com/heartinmind/AIChat.git
cd AIChat

# 환경 변수 설정
cp .env.example .env
echo "⚠️  .env 파일을 열어 CLAUDE_API_KEY를 입력하세요!"

# Backend 설정
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements_py313.txt

# Frontend 설정
cd ../frontend
npm install
npm run build

# Admin 설정
cd ../admin
npm install
npm run build

# PM2 설치 (프로세스 관리)
sudo npm install -g pm2

# PM2 ecosystem 파일 생성
cat > ecosystem.config.js << 'PMEOF'
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
      name: 'frontend',
      script: 'npm',
      args: 'start',
      cwd: './frontend',
      env: {
        PORT: 3002
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
    }
  ]
}
PMEOF

# PM2 시작
pm2 start ecosystem.config.js
pm2 save
pm2 startup

# Nginx 설정
sudo tee /etc/nginx/sites-available/elitebeauty << 'NGINXEOF'
server {
    listen 80;
    server_name YOUR_DOMAIN.com;

    # Frontend (User Chat)
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
NGINXEOF

# Nginx 활성화
sudo ln -s /etc/nginx/sites-available/elitebeauty /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

echo "✅ 서버 설정 완료!"
echo "다음 단계:"
echo "1. 도메인을 서버 IP로 연결"
echo "2. sudo certbot --nginx -d YOUR_DOMAIN.com 실행"
EOF

echo ""
echo "📌 배포 순서:"
echo "1. 서버 준비 (AWS EC2, DigitalOcean, Vultr 등)"
echo "2. SSH로 서버 접속"
echo "3. 위 server_setup.sh 내용 실행"
echo "4. 도메인 연결 및 SSL 설정"
echo ""
echo "🔧 환경 변수 업데이트 필요:"
echo "- frontend/.env.local"
echo "  NEXT_PUBLIC_API_URL=https://YOUR_DOMAIN.com"
echo ""
echo "- admin/src/contexts/AuthContext.tsx"
echo "  const API_BASE_URL = 'https://YOUR_DOMAIN.com';"
