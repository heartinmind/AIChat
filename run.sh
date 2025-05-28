#!/bin/bash

# 원스텝 실행 스크립트

echo "🚀 Elite Beauty Clinic AI 시스템을 시작합니다..."
echo ""

# 현재 디렉토리 확인
cd /Users/unipurple/Projects/AIChat

# 기존 프로세스 종료
echo "🧹 기존 프로세스를 정리합니다..."
pkill -f "python.*main.py" 2>/dev/null
pkill -f "node.*react-scripts" 2>/dev/null
sleep 2

# Python 가상환경 설정
echo "📦 Python 환경을 설정합니다..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Backend 설정
echo "🔧 Backend를 설정합니다..."
pip install --quiet --upgrade pip
pip install --quiet -r backend/requirements.txt

# .env 파일 생성
if [ ! -f ".env" ]; then
    echo "SECRET_KEY=dev-secret-key-12345" > .env
    echo "CLAUDE_API_KEY=your-api-key-here" >> .env
fi

# Admin 계정 생성
cd backend
python create_admin.py 2>/dev/null

# Backend 시작
echo "🚀 Backend를 시작합니다..."
python main.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Backend 시작 대기
sleep 3

# Frontend 설정
echo "🎨 Frontend를 설정합니다..."
cd admin

# npm 설치 확인
if [ ! -d "node_modules" ]; then
    rm -f package-lock.json
    npm install --legacy-peer-deps --silent
fi

# Frontend 시작
echo "🚀 Frontend를 시작합니다..."
npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!

# 시작 완료
echo ""
echo "✅ 시스템이 시작되었습니다!"
echo ""
echo "🌐 접속 정보:"
echo "   Admin Dashboard: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API 문서: http://localhost:8000/docs"
echo ""
echo "👤 로그인:"
echo "   이메일: admin@elitebeauty.com"
echo "   비밀번호: admin123"
echo ""
echo "📋 로그 확인:"
echo "   Backend: tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "🛑 종료: ./stop_system.sh"
echo ""

# 종료 시그널 처리
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

# 대기
wait
