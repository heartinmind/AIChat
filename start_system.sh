#!/bin/bash

# Elite Beauty Clinic AI 상담 시스템 시작 스크립트

echo "🚀 Elite Beauty Clinic AI 상담 시스템을 시작합니다..."

# 백엔드 디렉토리로 이동
cd /Users/unipurple/Projects/AIChat

# 가상환경 활성화
echo "📦 가상환경을 활성화합니다..."
source venv/bin/activate

# 필요한 패키지 설치
echo "📚 필요한 패키지를 확인합니다..."
pip install -r backend/requirements.txt

# Admin 계정 생성
echo "👤 Admin 계정을 생성합니다..."
cd backend
python create_admin.py

# PYTHONPATH 설정
export PYTHONPATH="/Users/unipurple/Projects/AIChat:$PYTHONPATH"

# 백엔드 서버 실행
echo "🔧 백엔드 서버를 시작합니다..."
python main.py &
BACKEND_PID=$!

# Admin 대시보드 디렉토리로 이동
cd ../admin

# npm 캐시 정리
echo "🧹 npm 캐시를 정리합니다..."
rm -rf node_modules package-lock.json

# npm 패키지 설치 (legacy peer deps 사용)
echo "📦 Admin 대시보드 패키지를 설치합니다..."
npm install --legacy-peer-deps

# Admin 대시보드 실행
echo "🎨 Admin 대시보드를 시작합니다..."
npm start &
FRONTEND_PID=$!

echo "✅ 시스템이 성공적으로 시작되었습니다!"
echo "🌐 Backend API: http://localhost:8000"
echo "🎨 Admin Dashboard: http://localhost:3000"
echo ""
echo "📧 Admin 로그인 정보:"
echo "   이메일: admin@elitebeauty.com"
echo "   비밀번호: admin123"
echo ""
echo "🛑 종료하려면 Ctrl+C를 누르세요"

# 프로세스 종료 대기
wait $BACKEND_PID
wait $FRONTEND_PID
